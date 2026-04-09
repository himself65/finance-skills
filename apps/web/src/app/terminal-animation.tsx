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

const accent = "var(--color-accent)";
const muted = "var(--color-text-muted)";
const secondary = "var(--color-text-secondary)";
const green = "var(--color-green)";

const terminalTabs: TabContent[] = [
  {
    label: "plugin",
    command: "npx plugins add himself65/finance-skills",
    lines: [
      { text: "", delay: 200 },
      { text: "┌   plugins", color: secondary, delay: 100 },
      { text: "◇  Source: https://github.com/himself65/finance-skills", color: muted, delay: 300 },
      { text: "│", color: muted, delay: 60 },
      { text: "●  Repository cloned", color: green, delay: 400 },
      { text: "│", color: muted, delay: 60 },
      { text: "◇  Found 1 plugin(s)", color: muted, delay: 300 },
      { text: "│", color: muted, delay: 60 },
      { text: "│  finance-skills  19 skills  Financial analysis and trading skills", color: secondary, delay: 100 },
      { text: "│", color: muted, delay: 60 },
      { text: "│  Targets:  Claude Code", color: muted, delay: 80 },
      { text: "│  Scope:    user", color: muted, delay: 80 },
      { text: "│", color: muted, delay: 60 },
      { text: "◆  Install? Y", color: secondary, delay: 500 },
      { text: "◇  Preparing plugins for Claude Code...", color: muted, delay: 400 },
      { text: "│", color: muted, delay: 60 },
      { text: "◇  Adding marketplace", color: muted, delay: 200 },
      { text: "●  Marketplace added", color: green, delay: 300 },
      { text: "│", color: muted, delay: 60 },
      { text: "◇  Installing finance-skills@finance-skills...", color: muted, delay: 400 },
      { text: "●  Installed finance-skills@finance-skills", color: green, delay: 300 },
      { text: "│", color: muted, delay: 60 },
      { text: "●  Done.  Restart your agent tools to load the plugins.", color: green, delay: 200 },
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
          height: minHeight,
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
        height: minHeight,
        transform: hasAnimated ? "translateY(0)" : "translateY(2rem)",
      }}
    >
      {/* Title bar */}
      <div className="flex shrink-0 items-center gap-2 px-4 py-3 border-b border-border">
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

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = scrollRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [visibleLines]);

  return (
    <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-4 font-mono text-sm leading-6">
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
