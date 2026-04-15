import styles from "./Hero.module.css";

export function Hero() {
  return (
    <section className={styles.hero}>
      <div className={`container ${styles.inner}`}>
        <h1 className={styles.title}>
          自信を、
          <br />
          もう一度。
        </h1>
        <p className={styles.subtitle}>
          最先端のスカルプマイクロピグメンテーション技術で
          <br />
          自然な仕上がりを実現します。
        </p>
        <a href="#contact" className={styles.ctaButton}>
          無料カウンセリングを予約する
        </a>
      </div>
    </section>
  );
}
