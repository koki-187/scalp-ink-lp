"use client";

import styles from "./Header.module.css";

export function Header() {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.inner}`}>
        <div className={styles.logo}>
          <span className={styles.logoText}>CIMA SKALP INK</span>
        </div>
        <nav className={styles.nav}>
          <a href="#features">特徴</a>
          <a href="#contact" className={styles.ctaButton}>
            無料カウンセリング
          </a>
        </nav>
      </div>
    </header>
  );
}
