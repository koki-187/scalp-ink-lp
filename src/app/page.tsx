import styles from "./page.module.css";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { Features } from "@/components/Features";
import { CTA } from "@/components/CTA";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <main className={styles.main}>
      <Header />
      <Hero />
      <Features />
      <CTA />
      <Footer />
    </main>
  );
}
