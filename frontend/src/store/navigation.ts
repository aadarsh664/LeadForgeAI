import { useState, useEffect } from "react";

export type PageId = "dashboard" | "workspace" | "businesses" | "people" | "campaigns" | "automation" | "ai" | "exports" | "settings" | "developer";

const NAV_EVENT = "leadforgeai_nav_change";

export function navigateTo(page: PageId) {
  localStorage.setItem("leadforgeai_current_page", page);
  window.dispatchEvent(new CustomEvent(NAV_EVENT, { detail: page }));
}

export function useNavigation() {
  const [currentPage, setCurrentPage] = useState<PageId>(() => {
    return (localStorage.getItem("leadforgeai_current_page") as PageId) || "dashboard";
  });

  useEffect(() => {
    const handleNav = (e: Event) => {
      const customEvent = e as CustomEvent<PageId>;
      setCurrentPage(customEvent.detail);
    };

    window.addEventListener(NAV_EVENT, handleNav);
    return () => window.removeEventListener(NAV_EVENT, handleNav);
  }, []);

  return { currentPage, navigateTo };
}
