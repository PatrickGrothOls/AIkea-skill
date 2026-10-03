/** Scope: Define a restrained optical filter shared by the viewer's glass overlays. */

// A declarative component lets React mount one inert SVG definition with the viewer.
export function ReviewGlassFilter() {
  return (
    <svg className="review-glass-filter" aria-hidden="true" focusable="false">
      <defs>
        <filter id="review-glass-refraction" x="0%" y="0%" width="100%" height="100%"
          colorInterpolationFilters="sRGB">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.028"
            numOctaves="1" seed="7" result="glass-map" />
          <feDisplacementMap in="SourceGraphic" in2="glass-map" scale="4"
            xChannelSelector="R" yChannelSelector="G" />
        </filter>
      </defs>
    </svg>
  );
}
