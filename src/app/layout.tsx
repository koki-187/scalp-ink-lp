import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CIMA SKALP INK | スカルプインク",
  description:
    "CIMA SKALP INK - 最先端のスカルプインク技術で自信を取り戻す。薄毛・抜け毛のお悩みに、自然な仕上がりのスカルプマイクロピグメンテーション。",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
