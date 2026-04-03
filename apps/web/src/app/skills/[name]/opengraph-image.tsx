import { ImageResponse } from "next/og";
import { skills, getSkill } from "@/data/skills";

export function generateStaticParams() {
  return skills.map((s) => ({ name: s.name }));
}

export const alt = "Finance Skills";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image({
  params,
}: {
  params: Promise<{ name: string }>;
}) {
  const { name } = await params;
  const skill = getSkill(name);
  const title = skill?.title ?? name;

  return new ImageResponse(
    (
      <div
        style={{
          background: "#0a0a0a",
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "Inter, sans-serif",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            fontSize: 64,
            fontWeight: 700,
            color: "#ededed",
            letterSpacing: "-0.02em",
          }}
        >
          <span>Finance Skills</span>
          <span style={{ color: "#888888" }}>/</span>
          <span style={{ color: "#0070f3" }}>{title}</span>
        </div>
        {skill && (
          <div
            style={{
              fontSize: 24,
              color: "#888888",
              marginTop: 16,
              maxWidth: 800,
              textAlign: "center",
              lineHeight: 1.4,
            }}
          >
            {skill.description}
          </div>
        )}
      </div>
    ),
    { ...size }
  );
}
