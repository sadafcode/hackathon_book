import React from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl'; // Import useBaseUrl
import styles from './index.module.css';

// Define a type for feature items
type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

// Define features for the book
const FeatureList: FeatureItem[] = [
  {
    title: 'Explore Embodied Intelligence',
    // Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default, // Removed
    description: (
      <>
        Delve into the core concepts of physical AI, understanding how intelligent
        algorithms interact with the real world through robotic forms.
      </>
    ),
  },
  {
    title: 'Master Robotics Platforms',
    // Svg: require('@site/static/img/undraw_docusaurus_react.svg').default, // Removed
    description: (
      <>
        Gain practical knowledge of leading robotics operating systems like ROS 2 and
        simulation environments such as Gazebo and NVIDIA Isaac Sim.
      </>
    ),
  },
  {
    title: 'Develop Humanoid Applications',
    // Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default, // Removed
    description: (
      <>
        Learn to design, program, and deploy AI solutions for humanoid robots,
        bridging the gap between digital intelligence and physical action.
      </>
    ),
  },
];

// Feature component to render each item
function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}> {/* Apply featureCard style */}
        <div className="text--center">
          {Svg && <Svg className={styles.featureSvg} role="img" />}
        </div>
        <div className="text--center padding-horiz--md">
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const backgroundImagePath = useBaseUrl('/img/ai_theme_background.png'); // Get the correct image URL

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <img
        src={backgroundImagePath}
        alt="AI Theme Background"
        className={styles.heroBackgroundImage}
      />
      <div className="container">
        <h1 className={styles.hero__title}>{siteConfig.title}</h1>
        <p className={styles.hero__subtitle}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--secondary button--lg', styles.customButton)}
            to="/introduction">
            Start Reading 🚀
          </Link>
        </div>
      </div>
    </header>
  );
}

// Main Home component
export default function Home(): JSX.Element {
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="A comprehensive textbook on Physical AI and Humanoid Robotics, bridging the digital brain and physical body.">
      <HomepageHeader />
      <main>
        <section className="container margin-top--lg">
          <div className="row">
            <div className={clsx('col col--12 text--center')}>
              <h2>Key Insights You'll Gain</h2>
              <p>Discover how to harness the power of AI to transform your entrepreneurial journey.</p>
            </div>
          </div>
        </section>
        {FeatureList && FeatureList.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {FeatureList.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}