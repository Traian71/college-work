// clic x y [dublu|dreapta]  -  click la coordonate de ecran (puncte), prin CGEvent
import Foundation
import CoreGraphics
let a = CommandLine.arguments
let p = CGPoint(x: Double(a[1])!, y: Double(a[2])!)
let mod = a.count > 3 ? a[3] : ""
let src = CGEventSource(stateID: .hidSystemState)
func ev(_ t: CGEventType, _ b: CGMouseButton, _ n: Int64) {
    let e = CGEvent(mouseEventSource: src, mouseType: t, mouseCursorPosition: p, mouseButton: b)!
    e.setIntegerValueField(.mouseEventClickState, value: n)
    e.post(tap: .cghidEventTap)
}
CGEvent(mouseEventSource: src, mouseType: .mouseMoved, mouseCursorPosition: p, mouseButton: .left)!.post(tap: .cghidEventTap)
usleep(80000)
if mod == "dreapta" { ev(.rightMouseDown, .right, 1); usleep(50000); ev(.rightMouseUp, .right, 1) }
else {
    ev(.leftMouseDown, .left, 1); usleep(50000); ev(.leftMouseUp, .left, 1)
    if mod == "dublu" { usleep(80000); ev(.leftMouseDown, .left, 2); usleep(50000); ev(.leftMouseUp, .left, 2) }
}
