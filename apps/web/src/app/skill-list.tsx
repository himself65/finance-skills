"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { Link } from "next-view-transitions";
import { motion, AnimatePresence, LayoutGroup } from "motion/react";
import type { Skill, PluginGroup } from "@/data/skills";
import { pluginGroupLabels, categoryLabels } from "@/data/skills";

const pluginOrder: PluginGroup[] = [
  "market-analysis",
  "social-readers",
  "data-providers",
  "startup-tools",
  "ui-tools",
];

type PluginFilter = "all" | PluginGroup;

const pluginFilters: { value: PluginFilter; label: string }[] = [
  { value: "all", label: "All" },
  ...pluginOrder.map((p) => ({
    value: p as PluginFilter,
    label: pluginGroupLabels[p],
  })),
];

function isValidPlugin(value: string | null): value is PluginGroup {
  return value !== null && pluginOrder.includes(value as PluginGroup);
}

export function SkillList({ skills }: { skills: Skill[] }) {
  const searchParams = useSearchParams();
  const initialPlugin = searchParams.get("plugin");
  const [activeFilter, setActiveFilter] = useState<PluginFilter>(
    isValidPlugin(initialPlugin) ? initialPlugin : "all"
  );

  const filtered =
    activeFilter === "all"
      ? skills
      : skills.filter((s) => s.plugin === activeFilter);

  const grouped = pluginOrder
    .map((p) => ({
      plugin: p,
      label: pluginGroupLabels[p],
      skills: filtered.filter((s) => s.plugin === p),
    }))
    .filter((g) => g.skills.length > 0);

  return (
    <div>
      {/* Filter bar — sticky */}
      <div className="sticky top-0 z-20 bg-bg/80 backdrop-blur-md flex items-center gap-3 py-3 -mx-6 px-6">
        <LayoutGroup>
          <div className="relative flex items-center gap-2 flex-wrap">
            {pluginFilters.map((f) => (
              <button
                key={f.value}
                onClick={() => setActiveFilter(f.value)}
                className={`relative z-10 px-3 py-1.5 text-xs font-medium rounded-full transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent ${
                  activeFilter === f.value
                    ? "text-white"
                    : "bg-bg-elevated text-text-secondary border border-border hover:border-text-muted"
                }`}
              >
                {activeFilter === f.value && (
                  <motion.div
                    layoutId="active-pill"
                    className="absolute inset-0 bg-accent rounded-full"
                    transition={{ type: "spring", duration: 0.4, bounce: 0.15 }}
                  />
                )}
                <span className="relative z-10">{f.label}</span>
              </button>
            ))}
          </div>
        </LayoutGroup>
        <motion.span
          key={filtered.length}
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-xs text-text-muted shrink-0"
        >
          {filtered.length} {filtered.length === 1 ? "skill" : "skills"}
        </motion.span>
      </div>

      {/* Plugin sections */}
      <div className="pb-16">
        <AnimatePresence mode="popLayout" initial={false}>
          {grouped.map((group) => (
            <motion.section
              key={group.plugin}
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.25, ease: "easeOut" }}
              className="mb-8"
            >
              <div className="flex items-center justify-between pb-3 border-b border-border">
                <h2 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                  {group.label}
                </h2>
              </div>
              <AnimatePresence mode="popLayout" initial={false}>
                {group.skills.map((skill) => (
                  <motion.div
                    key={skill.name}
                    layout
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 12 }}
                    transition={{ duration: 0.2, ease: "easeOut" }}
                    className="border-b border-border last:border-b-0"
                  >
                    <Link
                      href={`/skills/${skill.name}`}
                      className="flex items-center justify-between gap-4 py-4 hover:bg-bg-hover -mx-4 px-4 rounded transition-colors group"
                    >
                      <div className="min-w-0">
                        <span className="flex items-center gap-2">
                          <span className="font-medium text-sm group-hover:text-accent transition-colors">
                            {skill.name}
                          </span>
                          <span className="text-[10px] border border-border rounded px-1.5 py-0.5 text-text-muted">
                            {categoryLabels[skill.category]}
                          </span>
                          {skill.badge === "new" && (
                            <span className="text-[10px] font-semibold uppercase tracking-wider bg-accent/15 text-accent px-1.5 py-0.5 rounded">
                              New
                            </span>
                          )}
                          {skill.badge === "paid" && (
                            <span className="text-[10px] font-semibold uppercase tracking-wider bg-yellow/15 text-yellow px-1.5 py-0.5 rounded">
                              Paid
                            </span>
                          )}
                        </span>
                        <p className="text-xs text-text-muted mt-0.5 truncate">
                          {skill.description}
                        </p>
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </AnimatePresence>
            </motion.section>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
