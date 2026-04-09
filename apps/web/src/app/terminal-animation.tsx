"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface TerminalLine {
  text: string;
  color?: string;
  delay?: number;
}

export interface TabContent {
  label: string;
  command: string;
  lines: TerminalLine[];
}

// ---------------------------------------------------------------------------
// Context
// ---------------------------------------------------------------------------

interface TerminalAnimationContextValue {
  activeTab: number;
  setActiveTab: (index: number) => void;
  commandTyped: string;
  isTypingCommand: boolean;
  showCursor: boolean;
  visibleLines: number;
  currentTab: TabContent;
  tabs: TabContent[];
}

const TerminalAnimationContext = createContext<
  TerminalAnimationContextValue | undefined
>(undefined);

function useTerminalAnimation() {
  const ctx = useContext(TerminalAnimationContext);
  if (!ctx) {
    throw new Error(
      "TerminalAnimation components must be used within TerminalAnimationRoot"
    );
  }
  return ctx;
}

// ---------------------------------------------------------------------------
// Tab data
// ---------------------------------------------------------------------------

const terminalTabs: TabContent[] = [
  {
    label: "plugin",
    command: "npx plugins add himself65/finance-skills",
    lines: [
      { text: "", delay: 80 },
      {
        text: "  Resolving plugin himself65/finance-skills...",
        color: "var(--color-text-muted)",
        delay: 400,
      },
      {
        text: "  Found 27 skills across 6 categories",
        color: "var(--color-accent)",
        delay: 300,
      },
      { text: "", delay: 80 },
      {
        text: "  Installing plugin...",
        color: "var(--color-text-muted)",
        delay: 500,
      },
      {
        text: "  ✓ Plugin registered in .claude/settings.json",
        color: "var(--color-green)",
        delay: 200,
      },
      { text: "", delay: 80 },
      {
        text: "  Available categories:",
        color: "var(--color-text-secondary)",
        delay: 200,
      },
      {
        text: "    Analysis · Market Data · Risk · Sentiment · Strategy · Visualization",
        color: "var(--color-text-muted)",
        delay: 100,
      },
      { text: "", delay: 150 },
      {
        text: "  Done. All 27 skills are now available.",
        color: "var(--color-green)",
        delay: 300,
      },
    ],
  },
  {
    label: "skills",
    command: "npx skills add himself65/finance-skills",
    lines: [
      { text: "", delay: 80 },
      {
        text: "  Fetching skill registry...",
        color: "var(--color-text-muted)",
        delay: 400,
      },
      { text: "", delay: 80 },
      {
        text: "  Installing 27 skills:",
        color: "var(--color-text-secondary)",
        delay: 200,
      },
      {
        text: "  ✓ earnings-preview",
        color: "var(--color-green)",
        delay: 120,
      },
      {
        text: "  ✓ estimate-consensus",
        color: "var(--color-green)",
        delay: 80,
      },
      {
        text: "  ✓ options-payoff",
        color: "var(--color-green)",
        delay: 80,
      },
      {
        text: "  ✓ yfinance-reader",
        color: "var(--color-green)",
        delay: 80,
      },
      {
        text: "  ✓ hormuz-strait-monitor",
        color: "var(--color-green)",
        delay: 80,
      },
      {
        text: "  ✓ sepa-strategy  ... and 21 more",
        color: "var(--color-green)",
        delay: 80,
      },
      { text: "", delay: 150 },
      {
        text: "  27 skills installed to .claude/skills/",
        color: "var(--color-text-secondary)",
        delay: 300,
      },
    ],
  },
  {
    label: "single",
    command: "npx skills add himself65/finance-skills --skill earnings-preview",
    lines: [
      { text: "", delay: 80 },
      {
        text: "  Resolving skill earnings-preview...",
        color: "var(--color-text-muted)",
        delay: 400,
      },
      { text: "", delay: 80 },
      {
        text: "  earnings-preview",
        color: "var(--color-text-secondary)",
        delay: 200,
      },
      {
        text: "    Category:  Analysis",
        color: "var(--color-text-muted)",
        delay: 100,
      },
      {
        text: "    Platform:  CLI",
        color: "var(--color-text-muted)",
        delay: 80,
      },
      {
        text: "    Size:      4.2 kB",
        color: "var(--color-text-muted)",
        delay: 80,
      },
      { text: "", delay: 150 },
      {
        text: "  ✓ Installed to .claude/skills/earnings-preview/",
        color: "var(--color-green)",
        delay: 300,
      },
      { text: "", delay: 100 },
      {
        text: "  Try it: ask Claude about upcoming earnings for any ticker",
        color: "var(--color-text-muted)",
        delay: 200,
      },
    ],
  },
];

// ---------------------------------------------------------------------------
// Root
// ---------------------------------------------------------------------------

function TerminalAnimationRoot({
  tabs,
  children,
}: {
  tabs: TabContent[];
  children: ReactNode;
}) {
  const [activeTab, setActiveTab] = useState(0);
  const [visibleLines, setVisibleLines] = useState(0);
  const [commandTyped, setCommandTyped] = useState("");
  const [isTypingCommand, setIsTypingCommand] = useState(true);
  const [showCursor, setShowCursor] = useState(true);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>[]>([]);

  const clearTimeouts = useCallback(() => {
    timeoutRef.current.forEach(clearTimeout);
    timeoutRef.current = [];
  }, []);

  const animateTab = useCallback(
    (tabIndex: number) => {
      clearTimeouts();
      setVisibleLines(0);
      setCommandTyped("");
      setIsTypingCommand(true);
      setShowCursor(true);

      const tab = tabs[tabIndex];
      if (!tab) return;

      const command = tab.command;
      let charIndex = 0;

      const typeCommand = () => {
        if (charIndex <= command.length) {
          setCommandTyped(command.slice(0, charIndex));
          charIndex++;
          const t = setTimeout(typeCommand, 25 + Math.random() * 35);
          timeoutRef.current.push(t);
        } else {
          const t = setTimeout(() => {
            setIsTypingCommand(false);
            showLines(0);
          }, 250);
          timeoutRef.current.push(t);
        }
      };

      const showLines = (lineIndex: number) => {
        if (lineIndex <= tab.lines.length) {
          setVisibleLines(lineIndex);
          if (lineIndex < tab.lines.length) {
            const delay = tab.lines[lineIndex].delay ?? 100;
            const t = setTimeout(() => showLines(lineIndex + 1), delay);
            timeoutRef.current.push(t);
          } else {
            const t = setTimeout(() => setShowCursor(false), 600);
            timeoutRef.current.push(t);
          }
        }
      };

      const t = setTimeout(typeCommand, 300);
      timeoutRef.current.push(t);
    },
    [clearTimeouts, tabs]
  );

  useEffect(() => {
    animateTab(activeTab);
    return clearTimeouts;
  }, [activeTab, animateTab, clearTimeouts]);

  const currentTab = tabs[activeTab] ?? tabs[0];

  return (
    <TerminalAnimationContext.Provider
      value={{
        activeTab,
        setActiveTab,
        commandTyped,
        isTypingCommand,
        showCursor,
        visibleLines,
        currentTab,
        tabs,
      }}
    >
      {children}
    </TerminalAnimationContext.Provider>
  );
}

// ---------------------------------------------------------------------------
// Subcomponents
// ---------------------------------------------------------------------------

function TerminalWindow({
  children,
  minHeight = "20rem",
  variant = "standalone",
}: {
  children: ReactNode;
  minHeight?: string;
  variant?: "standalone" | "card";
}) {
  const windowRef = useRef<HTMLDivElement>(null);
  const [hasAnimated, setHasAnimated] = useState(false);

  useEffect(() => {
    const el = windowRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting) setHasAnimated(true);
      },
      { threshold: 0.1 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  if (variant === "card") {
    return (
      <div
        ref={windowRef}
        className="relative flex flex-col overflow-hidden transition-transform duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)]"
        style={{
          minHeight,
          transform: hasAnimated ? "translateY(0)" : "translateY(2rem)",
        }}
      >
        {children}
      </div>
    );
  }

  return (
    <div
      ref={windowRef}
      className="relative flex flex-col overflow-hidden rounded-xl border border-border bg-bg-elevated transition-transform duration-1000 ease-[cubic-bezier(0.16,1,0.3,1)]"
      style={{
        minHeight,
        transform: hasAnimated ? "translateY(0)" : "translateY(2rem)",
      }}
    >
      {/* Title bar */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
        <span className="w-3 h-3 rounded-full bg-[#ff5f57]" />
        <span className="w-3 h-3 rounded-full bg-[#febc2e]" />
        <span className="w-3 h-3 rounded-full bg-[#28c840]" />
        <span className="ml-2 text-xs text-text-muted font-mono">terminal</span>
      </div>
      {children}
    </div>
  );
}

function TerminalTabList() {
  const { activeTab, setActiveTab, tabs } = useTerminalAnimation();

  if (tabs.length <= 1) return null;

  return (
    <div className="flex gap-1 px-4 pt-3" role="tablist" aria-label="Terminal commands">
      {tabs.map((tab, i) => (
        <button
          key={tab.label}
          role="tab"
          aria-selected={activeTab === i}
          onClick={() => setActiveTab(i)}
          className={`px-3 py-1.5 text-xs font-mono rounded-md transition-colors ${
            activeTab === i
              ? "bg-accent text-white"
              : "text-text-muted hover:text-text-secondary hover:bg-bg-hover"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

function TerminalContent() {
  const {
    commandTyped,
    isTypingCommand,
    showCursor,
    visibleLines,
    currentTab,
    activeTab,
  } = useTerminalAnimation();

  return (
    <div className="flex-1 px-5 py-4 font-mono text-sm leading-6">
      {/* Command line */}
      <div className="text-text-secondary">
        <span className="text-text-muted">$ </span>
        {commandTyped}
        {isTypingCommand && showCursor && (
          <span className="ml-0.5 inline-block w-[7px] h-[18px] translate-y-[3px] bg-text-secondary animate-caret-blink" />
        )}
      </div>

      {/* Output */}
      {!isTypingCommand && (
        <div aria-live="polite" role="log">
          {currentTab.lines.map((line, i) => {
            if (i >= visibleLines) return null;
            return (
              <div key={`${activeTab}-${i}`}>
                <span style={line.color ? { color: line.color } : undefined}>
                  {line.text || "\u00A0"}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {/* Trailing cursor */}
      {!isTypingCommand &&
        showCursor &&
        visibleLines >= currentTab.lines.length && (
          <div className="text-text-secondary mt-1">
            <span className="text-text-muted">$ </span>
            <span className="ml-0.5 inline-block w-[7px] h-[18px] translate-y-[3px] bg-text-secondary animate-caret-blink" />
          </div>
        )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Composed export
// ---------------------------------------------------------------------------

export function TerminalAnimation({
  tabs = terminalTabs,
  minHeight,
  variant,
}: {
  tabs?: TabContent[];
  minHeight?: string;
  variant?: "standalone" | "card";
} = {}) {
  return (
    <TerminalAnimationRoot tabs={tabs}>
      <TerminalWindow minHeight={minHeight} variant={variant}>
        <TerminalTabList />
        <TerminalContent />
      </TerminalWindow>
    </TerminalAnimationRoot>
  );
}
