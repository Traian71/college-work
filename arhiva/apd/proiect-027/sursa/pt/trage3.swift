import Foundation
import CoreGraphics
let a = CommandLine.arguments.dropFirst().map { Double($0)! }
let p1 = CGPoint(x: a[0], y: a[1]), p2 = CGPoint(x: a[2], y: a[3])
let src = CGEventSource(stateID: .combinedSessionState)
func ev(_ t: CGEventType, _ p: CGPoint) { let e = CGEvent(mouseEventSource: src, mouseType: t, mouseCursorPosition: p, mouseButton: .left)!; e.setIntegerValueField(.mouseEventClickState, value: 1); e.post(tap: .cghidEventTap) }
ev(.mouseMoved, p1); usleep(300000)
ev(.leftMouseDown, p1); usleep(700000)
for i in 1...10 { ev(.leftMouseDragged, CGPoint(x: p1.x + Double(i), y: p1.y)); usleep(40000) }
let q = CGPoint(x: p1.x + 10, y: p1.y)
for i in 1...60 { let t = Double(i) / 60; ev(.leftMouseDragged, CGPoint(x: q.x + (p2.x - q.x) * t, y: q.y + (p2.y - q.y) * t)); usleep(30000) }
for _ in 0..<15 { ev(.leftMouseDragged, p2); usleep(40000) }
ev(.leftMouseUp, p2)
