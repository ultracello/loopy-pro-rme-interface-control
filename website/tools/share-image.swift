// Draws the picture that social networks show next to a link to the page (1200 x 630, see og:image in build.mjs).
// It carries the title of the page and the controller screenshot, so draw it again when either changes:
//   swift tools/share-image.swift public/controller-interface-page.png public/share-preview-babyface-pro-fs-loopy-pro.png
import AppKit

let a = CommandLine.arguments
guard a.count == 3, let shot = NSImage(contentsOfFile: a[1])?.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("usage: share-image.swift <screenshot.png> <out.png>"); exit(1) }
let W = 1200, H = 630
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
func rgb(_ hex: Int) -> CGColor { CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255, blue: CGFloat(hex & 255) / 255, alpha: 1) }
// from here on y runs downwards, as on the page
ctx.translateBy(x: 0, y: CGFloat(H)); ctx.scaleBy(x: 1, y: -1)
ctx.setFillColor(rgb(0x161614)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))

// the controller page without Loopy Pro's own bars, whole, on the right
let part = shot.cropping(to: CGRect(x: 232, y: 70, width: 1080, height: 898))!
let h: CGFloat = 566, w = (h * 1080 / 898).rounded(), frame = CGRect(x: CGFloat(W) - w - 36, y: 32, width: w, height: h)
ctx.saveGState()
ctx.addPath(CGPath(roundedRect: frame, cornerWidth: 14, cornerHeight: 14, transform: nil)); ctx.clip()
ctx.setFillColor(rgb(0x000000)); ctx.fill(frame)
ctx.interpolationQuality = .high
ctx.translateBy(x: frame.minX, y: frame.maxY); ctx.scaleBy(x: 1, y: -1)
ctx.draw(part, in: CGRect(x: 0, y: 0, width: w, height: h))
ctx.restoreGState()
ctx.addPath(CGPath(roundedRect: frame.insetBy(dx: 0.5, dy: 0.5), cornerWidth: 14, cornerHeight: 14, transform: nil))
ctx.setStrokeColor(rgb(0x34332f)); ctx.setLineWidth(1); ctx.strokePath()

// the mark of the page (favicon.svg)
let x0: CGFloat = 56
ctx.setFillColor(rgb(0x183c35)); ctx.addPath(CGPath(roundedRect: CGRect(x: x0, y: 64, width: 64, height: 64), cornerWidth: 14, cornerHeight: 14, transform: nil)); ctx.fillPath()
ctx.setFillColor(rgb(0xc9f187))
for (x, y, hh) in [(14.0, 18.0, 30.0), (28.0, 10.0, 35.0), (42.0, 23.0, 26.0)] { ctx.addPath(CGPath(roundedRect: CGRect(x: x0 + x, y: 64 + y, width: 8, height: hh), cornerWidth: 4, cornerHeight: 4, transform: nil)) }
ctx.fillPath()

// title and one line below it
NSGraphicsContext.current = NSGraphicsContext(cgContext: ctx, flipped: true)
func text(_ s: String, size: CGFloat, weight: NSFont.Weight, color: Int, y: CGFloat, spacing: CGFloat = 0) -> CGFloat {
  let style = NSMutableParagraphStyle(); style.lineSpacing = spacing
  let t = NSAttributedString(string: s, attributes: [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: NSColor(cgColor: rgb(color))!, .paragraphStyle: style, .kern: size > 30 ? -0.6 : 0])
  let box = t.boundingRect(with: CGSize(width: 400, height: 600), options: [.usesLineFragmentOrigin])
  t.draw(with: CGRect(x: x0, y: y, width: 400, height: 600), options: [.usesLineFragmentOrigin])
  return y + box.height
}
var y = text("RME Babyface\nPro FS,\ncontrolled from\nLoopy Pro", size: 46, weight: .bold, color: 0xecebe6, y: 176, spacing: 2)
y = text("On the iPad, without TotalMix FX.\nWhat works, what is measured,\nand a protocol reference.", size: 21, weight: .regular, color: 0xa9a8a0, y: y + 26, spacing: 5)

let rep = NSBitmapImageRep(cgImage: ctx.makeImage()!)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
print("written \(W)x\(H), text ends at y=\(Int(y))")
