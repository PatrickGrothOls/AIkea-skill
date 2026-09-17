/** Scope: Render the viewer identity in its native sans-serif and glass palette. */

import { Component } from "react";

export class ReviewBrand extends Component {
  render() {
    return (
      <svg className="review-brand" viewBox="0 0 300 88"
        role="img" aria-label="AIkea" focusable="false">
        <defs>
          <text id="brand-kea" x="105" y="75" textLength="183"
            lengthAdjust="spacingAndGlyphs">kea</text>
          <mask id="brand-field" maskUnits="userSpaceOnUse"
            x="98" y="0" width="202" height="88" style={{ maskType: "luminance" }}>
            <rect x="98" y="0" width="202" height="88" fill="white" />
            <use href="#brand-kea" fill="black" />
          </mask>
          <linearGradient id="brand-glass" x1="0" y1="0" x2="1" y2="1">
            <stop stopColor="#fffdf8" stopOpacity=".55" />
            <stop offset=".5" stopColor="#f2f6f2" stopOpacity=".35" />
            <stop offset="1" stopColor="#fffdf8" stopOpacity=".5" />
          </linearGradient>
        </defs>
        <text x="0" y="75" textLength="93" lengthAdjust="spacingAndGlyphs"
          fill="currentColor">AI</text>
        <rect x="98" y="0" width="202" height="88" rx="5"
          fill="currentColor" mask="url(#brand-field)" />
        <use href="#brand-kea" fill="url(#brand-glass)" />
      </svg>
    );
  }
}
