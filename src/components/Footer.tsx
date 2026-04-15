import styles from "./Footer.module.css";

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.inner}`}>
        <p className={styles.copyright}>
          &copy; {new Date().getFullYear()} CIMA SKALP INK. All rights
          reserved.
        </p>
      </div>
    </footer>
  );
}
