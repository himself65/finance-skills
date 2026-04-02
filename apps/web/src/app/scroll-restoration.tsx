"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";

const scrollPositions = new Map<string, number>();

export function ScrollRestoration() {
  const pathname = usePathname();
  const prevPathname = useRef(pathname);

  // Save scroll position on scroll events
  useEffect(() => {
    const save = () => {
      scrollPositions.set(pathname, window.scrollY);
    };

    window.addEventListener("scroll", save, { passive: true });
    return () => window.removeEventListener("scroll", save);
  }, [pathname]);

  // Restore scroll position after navigation
  useEffect(() => {
    if (prevPathname.current !== pathname) {
      const saved = scrollPositions.get(pathname);
      if (saved !== undefined) {
        // Wait for the view transition animation to finish (300ms total)
        // before restoring, so the transition doesn't override scroll.
        setTimeout(() => window.scrollTo(0, saved), 350);
      }
      prevPathname.current = pathname;
    }
  }, [pathname]);

  return null;
}
