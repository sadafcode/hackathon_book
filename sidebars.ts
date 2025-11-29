import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
    tutorialSidebar: [
    {
      type: 'category',
      label: 'Part 1: Foundations of Physical AI & Humanoid Robotics',
      link: {type: 'generated-index', title: 'Part 1 Overview'},
      items: [
        '01-introduction-to-physical-ai-humanoid-robotics',
        '02-the-robotic-nervous-system',
      ],
    },
    {
      type: 'category',
      label: 'Part 2: Simulation & Perception',
      link: {type: 'generated-index', title: 'Part 2 Overview'},
      items: [
        '03-the-digital-twin',
        '04-the-ai-robot-brain',
      ],
    },
    {
      type: 'category',
      label: 'Part 3: Advanced Humanoid Robotics & Conversational AI',
      link: {type: 'generated-index', title: 'Part 3 Overview'},
      items: [
        '05-humanoid-robot-development',
        '06-vision-language-action-conversational-robotics',
      ],
    },
    {
      type: 'category',
      label: 'Part 4: Appendices & Projects',
      link: {type: 'generated-index', title: 'Part 4 Overview'},
      items: [
        'appendix-a-hardware-requirements-lab-setup',
        'appendix-b-assessments',
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
