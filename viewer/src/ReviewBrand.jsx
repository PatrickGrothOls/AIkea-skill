/** Scope: Composite the approved logo silhouette with petrol and translucent gold. */

import { Component } from "react";
import silhouette from "./assets/approved-logo.png";

export class ReviewBrand extends Component {
  render() {
    return (
      <svg className="review-brand" viewBox="145 270 1246 394"
        role="img" aria-label="AIkea" focusable="false">
        <defs>
          {/* The original green channel separates red/black ink from white. */}
          <filter id="brand-ink" colorInterpolationFilters="sRGB">
            <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 -2 0 2 0" />
            <feComponentTransfer>
              <feFuncA type="linear" slope="1.1" intercept="-.1" />
            </feComponentTransfer>
          </filter>
          <filter id="brand-cutout" colorInterpolationFilters="sRGB">
            <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 2 0 -1 0" />
          </filter>
          <mask id="brand-positive" maskUnits="userSpaceOnUse"
            x="0" y="0" width="1536" height="1024" style={{ maskType: "alpha" }}>
            <image href={silhouette} width="1536" height="1024" filter="url(#brand-ink)" />
          </mask>
          <mask id="brand-negative" maskUnits="userSpaceOnUse"
            x="638" y="274" width="751" height="386" style={{ maskType: "alpha" }}>
            <image href={silhouette} width="1536" height="1024" filter="url(#brand-cutout)" />
          </mask>
          <linearGradient id="brand-petrol" x1="0" y1="0" x2="1" y2="0">
            <stop stopColor="#14252d" />
            <stop offset="1" stopColor="#28565b" />
          </linearGradient>
          <linearGradient id="brand-gold" x1="0" y1="0" x2="1" y2="1">
            <stop stopColor="#b79961" stopOpacity=".48" />
            <stop offset=".5" stopColor="#eedab0" stopOpacity=".60" />
            <stop offset="1" stopColor="#c5a66c" stopOpacity=".48" />
          </linearGradient>
        </defs>
        <rect x="145" y="270" width="1246" height="394"
          fill="url(#brand-petrol)" mask="url(#brand-positive)" />
        <rect x="638" y="274" width="751" height="386"
          fill="url(#brand-gold)" mask="url(#brand-negative)" />
      </svg>
    );
  }
}
