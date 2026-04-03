import { ImageResponse } from "next/og";

export const alt = "Finance Skills";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default function Image() {
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
            fontSize: 72,
            fontWeight: 700,
            color: "#ededed",
            letterSpacing: "-0.02em",
          }}
        >
          Finance Skills
        </div>
        <div
          style={{
            fontSize: 28,
            color: "#888888",
            marginTop: 16,
          }}
        >
          Financial analysis skills for AI agents
        </div>
      </div>
    ),
    { ...size }
  );
}
