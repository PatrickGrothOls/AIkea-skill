/** Scope: Display the approved logo silhouette without replacing its lettering. */

import { Component } from "react";
import approvedLogo from "./assets/aikea-approved-logo.jpg";

export class ReviewBrand extends Component {
  render() {
    return (
      <svg className="review-brand" viewBox="124 235 1078 350"
        role="img" aria-label="AIkea" focusable="false">
        <defs>
          {/* Separate dark ink from the light reference background, preserving contours. */}
          <filter id="brand-ink" colorInterpolationFilters="sRGB">
            <feColorMatrix type="matrix" values="
              -1 -1 -1 0 1.5
              -1 -1 -1 0 1.5
              -1 -1 -1 0 1.5
               0  0  0 1 0" />
          </filter>
          <mask id="brand-silhouette" maskUnits="userSpaceOnUse"
            x="124" y="235" width="1078" height="350"
            style={{ maskType: "luminance" }}>
            <image href={approvedLogo} width="1280" height="853"
              filter="url(#brand-ink)" />
          </mask>
        </defs>
        <rect x="124" y="235" width="1078" height="350"
          fill="currentColor" mask="url(#brand-silhouette)" />
      </svg>
    );
  }
}
