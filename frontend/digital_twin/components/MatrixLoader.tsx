"use client";

import { useEffect, useState } from "react";

const CHARS = "01アイウエオカキクケコサシスセソタチツテトABCDEF#$%&";

function randomChar() {
  return CHARS[Math.floor(Math.random() * CHARS.length)];
}

export default function MatrixLoader({
  cols = 12,
  rows = 1,
  label = "",
}: {
  cols?: number;
  rows?: number;
  label?: string;
}) {
  const total = cols * rows;

  // Start with a fixed placeholder so server and client render the same HTML
  const [cells, setCells] = useState<string[]>(() =>
    Array.from({ length: total }, () => "0")
  );

  useEffect(() => {
    // Fill with random characters only after mounting in the browser
    setCells(Array.from({ length: total }, () => randomChar()));

    const id = setInterval(() => {
      setCells((prev) =>
        prev.map((c) => (Math.random() < 0.3 ? randomChar() : c))
      );
    }, 80);
    return () => clearInterval(id);
  }, [total]);

  return (
    <div className="matrix-loader" aria-label="Loading" role="status">
      <div
        className="matrix-grid"
        style={{ gridTemplateColumns: `repeat(${cols}, 1fr)` }}
      >
        {cells.map((c, i) => (
          <span key={i} className="matrix-cell matrix-cell-random">
            {c}
          </span>
        ))}
      </div>
      {label && <span className="matrix-label">{label}</span>}
    </div>
  );
}