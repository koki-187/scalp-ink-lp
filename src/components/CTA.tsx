import styles from "./CTA.module.css";

export function CTA() {
  return (
    <section id="contact" className={`section ${styles.cta}`}>
      <div className={`container ${styles.inner}`}>
        <h2 className={styles.title}>まずは無料カウンセリングから</h2>
        <p className={styles.description}>
          お悩みやご質問など、お気軽にご相談ください。
          <br />
          専門スタッフが丁寧にご対応いたします。
        </p>
        <a href="#" className={styles.ctaButton}>
          無料カウンセリングを予約する
        </a>
      </div>
    </section>
  );
}
