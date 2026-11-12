# coding:utf-8
import math
import os
from ctypes import (CDLL, CFUNCTYPE, POINTER, Structure, Union, addressof,
                    c_char_p, c_int, c_int32, c_uint32, c_void_p)
from dataclasses import dataclass
from functools import lru_cache

import xcffib as xcb
from PyQt5 import sip
from PyQt5.QtCore import QByteArray, QEvent, QObject, Qt
from PyQt5.QtGui import QGuiApplication, QPlatformSurfaceEvent
from PyQt5.QtX11Extras import QX11Info
from xcffib.xproto import Atom, ImageFormat, PropMode, xprotoExtension

# left, top, right, bottom
PADDING = (30, 25, 30, 35)

WL_MARSHAL_FLAG_DESTROY = 1
WL_SHM_FORMAT_ARGB8888 = 0
SHADOW_COMMIT, SHADOW_ATTACH_LEFT, SHADOW_SET_LEFT_OFFSET, SHADOW_DESTROY = 0, 1, 9, 13
MANAGER_CREATE, MANAGER_UNSET = 0, 1


def addShadow(window):
    """ add KWin shadow to window

    Parameters
    ----------
    window: QWidget
        top level window to add shadow
    """
    platform = QGuiApplication.platformName()
    if platform.startswith("wayland"):
        kwinShadow = createKwinShadow()
        if kwinShadow and not window.findChild(WaylandWindowShadow, options=Qt.FindDirectChildrenOnly):
            WaylandWindowShadow(window, kwinShadow)
    elif platform == "xcb":
        x11Shadow = createX11Shadow()
        if x11Shadow and not window.findChild(X11WindowShadow, options=Qt.FindDirectChildrenOnly):
            X11WindowShadow(window, x11Shadow)


def removeShadow(window):
    """ remove shadow from window

    Parameters
    ----------
    window: QWidget
        top level window to remove shadow
    """
    windowShadow = window.findChild((WaylandWindowShadow, X11WindowShadow), options=Qt.FindDirectChildrenOnly)
    if windowShadow:
        windowShadow.remove()


@dataclass(frozen=True)
class Tile:
    width: int
    height: int
    pixels: bytes  # premultiplied ARGB8888


@dataclass(frozen=True)
class Tiles:
    left: Tile
    topLeft: Tile
    top: Tile
    topRight: Tile
    right: Tile
    bottomRight: Tile
    bottom: Tile
    bottomLeft: Tile


def buildTiles():
    left, top, right, bottom = PADDING
    # Breeze "Large" shadow: (sigma, y offset, opacity)
    layers = ((10.0, 5, 0.22), (5.0, 2, 0.12))
    # corner tiles extend until the falloff ends
    inset = 35

    def cdf(z):
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    def horizontal(x, side, sigma):
        if side == "middle":
            return 1.0
        if side == "left":
            return cdf((x + 0.5) / sigma)
        return cdf(-(x + 0.5) / sigma)

    def vertical(y, side, sigma, offset):
        if side == "middle":
            return 1.0
        if side == "top":
            return cdf((y + 0.5 - offset) / sigma)
        return cdf((offset - y - 0.5) / sigma)

    def build(columns, columnSide, rows, rowSide):
        alphas = [
            (opacity, [horizontal(x, columnSide, sigma) for x in columns],
             [vertical(y, rowSide, sigma, offset) for y in rows])
            for sigma, offset, opacity in layers
        ]
        pixels = bytearray(len(columns) * len(rows) * 4)
        index = 3
        for row in range(len(rows)):
            for column in range(len(columns)):
                transparency = 1.0
                for opacity, xs, ys in alphas:
                    transparency *= 1 - opacity * xs[column] * ys[row]
                pixels[index] = round(255 * (1 - transparency))
                index += 4
        return Tile(len(columns), len(rows), bytes(pixels))

    leftColumns, rightColumns, middle = range(-left, inset), range(-inset, right), range(1)
    topRows, bottomRows = range(-top, inset), range(-inset, bottom)
    return Tiles(
        left=build(range(-left, 0), "left", middle, "middle"),
        topLeft=build(leftColumns, "left", topRows, "top"),
        top=build(middle, "middle", range(-top, 0), "top"),
        topRight=build(rightColumns, "right", topRows, "top"),
        right=build(range(right), "right", middle, "middle"),
        bottomRight=build(rightColumns, "right", bottomRows, "bottom"),
        bottom=build(middle, "middle", range(bottom), "bottom"),
        bottomLeft=build(leftColumns, "left", bottomRows, "bottom"),
    )


class X11Shadow:
    def __init__(self, conn, atom, data):
        self.conn = conn
        self.atom = atom
        self.data = data

    def set(self, handle):
        xprotoExtension(self.conn).ChangeProperty(
            PropMode.Replace, int(handle.winId()), self.atom, Atom.CARDINAL, 32, len(self.data), self.data)
        self.conn.flush()

    def unset(self, handle):
        xprotoExtension(self.conn).DeleteProperty(int(handle.winId()), self.atom)
        self.conn.flush()


class X11WindowShadow(QObject):
    def __init__(self, window, x11Shadow):
        super().__init__(window)
        self.x11Shadow = x11Shadow
        self.handle = window.windowHandle()
        self.handle.installEventFilter(self)
        self.set()

    def eventFilter(self, handle, event):
        # Qt recreates the X window after WindowStaysOnTopHint changes
        if event.type() == QEvent.Expose and int(handle.winId()) != self.winId:
            self.set()

        return False

    def set(self):
        self.winId = int(self.handle.winId())
        self.x11Shadow.set(self.handle)

    def remove(self):
        self.handle.removeEventFilter(self)
        self.x11Shadow.unset(self.handle)
        self.setParent(None)
        self.deleteLater()


@lru_cache(maxsize=None)
def createX11Shadow():
    conn = xcb.wrap(sip.unwrapinstance(QX11Info.connection()))
    xproto = xprotoExtension(conn)
    root = QX11Info.appRootWindow(QX11Info.appScreen())

    def internAtom(name):
        return xproto.InternAtom(False, len(name), name).reply().atom

    atom = internAtom("_KDE_NET_WM_SHADOW")
    supported = xproto.GetProperty(
        False, root, internAtom("_NET_SUPPORTED"), Atom.ATOM, 0, 4096).reply().value.to_atoms()
    if atom not in supported:
        return None

    built = buildTiles()
    pixmaps = []
    for tile in (built.top, built.topRight, built.right, built.bottomRight,
                 built.bottom, built.bottomLeft, built.left, built.topLeft):
        pixmap, gc = conn.generate_id(), conn.generate_id()
        xproto.CreatePixmap(32, pixmap, root, tile.width, tile.height)
        xproto.CreateGC(gc, pixmap, 0, [])
        xproto.PutImage(ImageFormat.ZPixmap, pixmap, gc, tile.width, tile.height,
                        0, 0, 0, 32, len(tile.pixels), tile.pixels)
        xproto.FreeGC(gc)
        pixmaps.append(pixmap)

    left, top, right, bottom = PADDING
    conn.flush()
    return X11Shadow(conn, atom, [*pixmaps, top, right, bottom, left])


class WlMessage(Structure):
    _fields_ = [("name", c_char_p), ("signature", c_char_p), ("types", POINTER(c_void_p))]


class WlInterface(Structure):
    _fields_ = [
        ("name", c_char_p), ("version", c_int),
        ("method_count", c_int), ("methods", POINTER(WlMessage)),
        ("event_count", c_int), ("events", POINTER(WlMessage)),
    ]


class WlArgument(Union):
    _fields_ = [("i", c_int32), ("s", c_char_p), ("o", c_void_p)]


GlobalListener = CFUNCTYPE(None, c_void_p, c_void_p, c_uint32, c_char_p, c_uint32)
GlobalRemoveListener = CFUNCTYPE(None, c_void_p, c_void_p, c_uint32)


class RegistryListener(Structure):
    _fields_ = [("global_", GlobalListener), ("global_remove", GlobalRemoveListener)]


# refer to: https://invent.kde.org/libraries/plasma-wayland-protocols/-/blob/master/src/protocols/shadow.xml
class Protocol:
    def __init__(self, wayland):
        surfaceInterface = addressof(WlInterface.in_dll(wayland, "wl_surface_interface"))
        bufferInterface = addressof(WlInterface.in_dll(wayland, "wl_buffer_interface"))
        self.arrays = []
        self.shadow = self.buildInterface(b"org_kde_kwin_shadow", 2, [
            (b"commit", b"", []),
            *[(b"attach_" + side, b"o", [bufferInterface]) for side in (
                b"left", b"top_left", b"top", b"top_right", b"right", b"bottom_right", b"bottom", b"bottom_left")],
            *[(b"set_" + side + b"_offset", b"f", [None]) for side in (b"left", b"top", b"right", b"bottom")],
            (b"destroy", b"2", []),
        ])
        self.manager = self.buildInterface(b"org_kde_kwin_shadow_manager", 2, [
            (b"create", b"no", [addressof(self.shadow), surfaceInterface]),
            (b"unset", b"o", [surfaceInterface]),
            (b"destroy", b"2", []),
        ])

    def buildInterface(self, name, version, methods):
        messages = (WlMessage * len(methods))()
        self.arrays.append(messages)
        for message, (methodName, signature, types) in zip(messages, methods):
            typeArray = (c_void_p * max(len(types), 1))(*types)
            self.arrays.append(typeArray)
            message.name, message.signature, message.types = methodName, signature, typeArray
        return WlInterface(name, version, len(methods), messages, 0, None)


def marshal(wayland, proxy, opcode, args, interface=None, version=0, flags=0):
    array = (WlArgument * max(len(args), 1))()
    for argument, value in zip(array, args):
        if isinstance(value, bytes):
            argument.s = value
        elif isinstance(value, float):
            argument.i = round(value * 256)
        elif isinstance(value, int):
            argument.i = value
        else:
            argument.o = value
    if interface is not None and not version:
        version = wayland.wl_proxy_get_version(proxy)
    return wayland.wl_proxy_marshal_array_flags(
        proxy, opcode, addressof(interface) if interface is not None else None, version, flags, array)


class KwinShadow:
    def __init__(self, wayland, display, surfaceOf, protocol, manager, managerVersion, buffers):
        self.wayland = wayland
        self.display = display
        self.surfaceOf = surfaceOf
        self.protocol = protocol
        self.manager = manager
        self.managerVersion = managerVersion
        self.buffers = buffers

    def create(self, window):
        surface = self.surfaceOf(window)
        if not surface:
            return None

        wayland = self.wayland
        shadow = marshal(wayland, self.manager, MANAGER_CREATE, [None, c_void_p(surface)], self.protocol.shadow)
        for opcode, buffer in enumerate(self.buffers, start=SHADOW_ATTACH_LEFT):
            marshal(wayland, shadow, opcode, [c_void_p(buffer)])
        for opcode, offset in enumerate(PADDING, start=SHADOW_SET_LEFT_OFFSET):
            marshal(wayland, shadow, opcode, [float(offset)])
        marshal(wayland, shadow, SHADOW_COMMIT, [])
        wayland.wl_display_flush(self.display)

        # the shadow takes effect on the next commit
        window.requestUpdate()
        return shadow

    def destroy(self, shadow):
        if self.managerVersion >= 2:
            marshal(self.wayland, shadow, SHADOW_DESTROY, [], flags=WL_MARSHAL_FLAG_DESTROY)
        else:
            self.wayland.wl_proxy_destroy(shadow)
        self.wayland.wl_display_flush(self.display)

    def unset(self, window):
        surface = self.surfaceOf(window)
        if not surface:
            return

        marshal(self.wayland, self.manager, MANAGER_UNSET, [c_void_p(surface)])
        self.wayland.wl_display_flush(self.display)
        window.requestUpdate()


class WaylandWindowShadow(QObject):
    def __init__(self, window, kwinShadow):
        # the QWindow wrapper may be garbage collected
        super().__init__(window)
        self.kwinShadow = kwinShadow
        self.shadow = None
        self.handle = window.windowHandle()
        self.handle.installEventFilter(self)

    def eventFilter(self, window, event):
        et = event.type()
        isSurfaceGone = et == QEvent.Hide or (
            et == QEvent.PlatformSurface
            and event.surfaceEventType() == QPlatformSurfaceEvent.SurfaceAboutToBeDestroyed
        )
        if self.shadow is None and et == QEvent.Expose and window.isExposed():
            self.shadow = self.kwinShadow.create(window)
        elif self.shadow is not None and isSurfaceGone:
            self.kwinShadow.destroy(self.shadow)
            self.shadow = None

        return False

    def remove(self):
        self.handle.removeEventFilter(self)
        if self.shadow is not None:
            self.kwinShadow.unset(self.handle)
            self.kwinShadow.destroy(self.shadow)
            self.shadow = None

        self.setParent(None)
        self.deleteLater()


@lru_cache(maxsize=None)
def createKwinShadow():
    # Qt has no public API to get wl_surface
    try:
        wayland = CDLL("libwayland-client.so.0")
        nativeInterface = CDLL("libQt5Gui.so.5")["_ZN15QGuiApplication23platformNativeInterfaceEv"]
        waylandClient = CDLL("libQt5WaylandClient.so.5")
        resourceForIntegration = waylandClient[
            "_ZN15QtWaylandClient23QWaylandNativeInterface28nativeResourceForIntegrationERK10QByteArray"]
        resourceForWindow = waylandClient[
            "_ZN15QtWaylandClient23QWaylandNativeInterface23nativeResourceForWindowERK10QByteArrayP7QWindow"]
        wayland.wl_proxy_marshal_array_flags  # requires libwayland 1.20
    except (OSError, AttributeError):
        return None

    nativeInterface.restype = c_void_p
    resourceForIntegration.restype, resourceForIntegration.argtypes = c_void_p, [c_void_p, c_void_p]
    resourceForWindow.restype, resourceForWindow.argtypes = c_void_p, [c_void_p, c_void_p, c_void_p]
    wayland.wl_proxy_marshal_array_flags.restype = c_void_p
    wayland.wl_proxy_marshal_array_flags.argtypes = [
        c_void_p, c_uint32, c_void_p, c_uint32, c_uint32, POINTER(WlArgument)]
    wayland.wl_proxy_create_wrapper.restype = c_void_p
    wayland.wl_display_create_queue.restype = c_void_p
    for name in ("wl_proxy_get_version", "wl_proxy_create_wrapper", "wl_proxy_wrapper_destroy",
                 "wl_proxy_destroy", "wl_display_flush", "wl_display_create_queue"):
        getattr(wayland, name).argtypes = [c_void_p]
    for name in ("wl_proxy_set_queue", "wl_display_roundtrip_queue"):
        getattr(wayland, name).argtypes = [c_void_p, c_void_p]
    wayland.wl_proxy_add_listener.argtypes = [c_void_p, c_void_p, c_void_p]

    native = nativeInterface()

    surfaceName = QByteArray(b"surface")

    def surfaceOf(window):
        return resourceForWindow(native, sip.unwrapinstance(surfaceName), sip.unwrapinstance(window))

    def interface(name):
        return WlInterface.in_dll(wayland, name)

    displayName = QByteArray(b"wl_display")
    display = resourceForIntegration(native, sip.unwrapinstance(displayName))
    advertised = {}

    def onGlobal(data, registry, name, interfaceName, version):
        advertised[interfaceName] = (name, version)

    listener = RegistryListener(GlobalListener(onGlobal), GlobalRemoveListener(lambda *_: None))
    queue = wayland.wl_display_create_queue(display)
    wrapper = wayland.wl_proxy_create_wrapper(display)
    wayland.wl_proxy_set_queue(wrapper, queue)
    registry = marshal(wayland, wrapper, 1, [None], interface("wl_registry_interface"))
    wayland.wl_proxy_wrapper_destroy(wrapper)
    wayland.wl_proxy_add_listener(registry, addressof(listener), None)
    wayland.wl_display_roundtrip_queue(display, queue)

    if b"org_kde_kwin_shadow_manager" not in advertised or b"wl_shm" not in advertised:
        wayland.wl_proxy_destroy(registry)
        return None

    def bind(name, boundInterface, maxVersion):
        globalName, version = advertised[name]
        version = min(version, maxVersion)
        return marshal(wayland, registry, 0, [globalName, name, version, None], boundInterface, version), version

    protocol = Protocol(wayland)
    manager, managerVersion = bind(b"org_kde_kwin_shadow_manager", protocol.manager, 2)
    shm, _ = bind(b"wl_shm", interface("wl_shm_interface"), 1)
    wayland.wl_proxy_destroy(registry)

    built = buildTiles()
    tiles = (built.left, built.topLeft, built.top, built.topRight,
             built.right, built.bottomRight, built.bottom, built.bottomLeft)
    fd = os.memfd_create("qframelesswindow-shadow")
    try:
        for tile in tiles:
            os.write(fd, tile.pixels)
        pool = marshal(wayland, shm, 0, [None, fd, sum(len(tile.pixels) for tile in tiles)],
                       interface("wl_shm_pool_interface"))
    finally:
        os.close(fd)

    buffers, offset = [], 0
    for tile in tiles:
        buffers.append(marshal(wayland, pool, 0, [None, offset, tile.width, tile.height, tile.width * 4,
                                                  WL_SHM_FORMAT_ARGB8888], interface("wl_buffer_interface")))
        offset += len(tile.pixels)

    marshal(wayland, pool, 1, [], flags=WL_MARSHAL_FLAG_DESTROY)
    wayland.wl_display_flush(display)
    return KwinShadow(wayland, display, surfaceOf, protocol, manager, managerVersion, buffers)
