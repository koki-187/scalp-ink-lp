import styles from "./Features.module.css";

const features = [
  {
    title: "自然な仕上がり",
    description:
      "最新の技術と厳選されたインクで、地肌に馴染む自然な毛根を再現。周囲に気づかれない仕上がりを実現します。",
  },
  {
    title: "痛みが少ない",
    description:
      "独自の施術技法により、痛みを最小限に抑えた快適な施術を提供。初めての方でも安心してお受けいただけます。",
  },
  {
    title: "長持ちする効果",
    description:
      "高品質なインクと確かな技術で、長期間美しい状態を維持。メンテナンスの手間も最小限です。",
  },
];

export function Features() {
  return (
    <section id="features" className={`section ${styles.features}`}>
      <div className="container">
        <h2 className="section-title">選ばれる理由</h2>
        <div className={styles.grid}>
          {features.map((feature) => (
            <div key={feature.title} className={styles.card}>
              <h3 className={styles.cardTitle}>{feature.title}</h3>
              <p className={styles.cardDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
