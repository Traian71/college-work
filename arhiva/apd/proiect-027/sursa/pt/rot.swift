// rot x y n - rotita mouse-ului (n > 0 = sus)
import Foundation
import CoreGraphics
let a = CommandLine.arguments
let p = CGPoint(x: Double(a[1])!, y: Double(a[2])!)
CGEvent(mouseEventSource: nil, mouseType: .mouseMoved, mouseCursorPosition: p, mouseButton: .left)!.post(tap: .cghidEventTap)
usleep(100000)
let n = Int32(a[3])!
for _ in 0..<abs(n) { CGEvent(scrollWheelEvent2Source: nil, units: .line, wheelCount: 1, wheel1: n > 0 ? 5 : -5, wheel2: 0, wheel3: 0)!.post(tap: .cghidEventTap); usleep(30000) }
