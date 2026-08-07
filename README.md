<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Giovani Rodrigo - Developer & DevOps</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    :root {
      --primary: #2c5aa0;
      --secondary: #1a1a1a;
      --accent: #f0a000;
      --bg-dark: #0f0f0f;
      --bg-surface: #1a1a1a;
      --bg-card: #262626;
      --text-primary: #e8e8e8;
      --text-secondary: #b0b0b0;
      --text-muted: #707070;
      --border: #3a3a3a;
      --border-light: #4a4a4a;
      --success: #10b981;
      --warning: #f59e0b;
    }

    @media (prefers-color-scheme: light) {
      :root {
        --primary: #2c5aa0;
        --secondary: #ffffff;
        --accent: #f0a000;
        --bg-dark: #ffffff;
        --bg-surface: #f8f7f6;
        --bg-card: #ffffff;
        --text-primary: #1a1a1a;
        --text-secondary: #666;
        --text-muted: #999;
        --border: #e5e3e0;
        --border-light: #d5d3d0;
        --success: #059669;
        --warning: #d97706;
      }
    }

    [data-theme="light"] {
      --primary: #2c5aa0;
      --secondary: #ffffff;
      --accent: #f0a000;
      --bg-dark: #ffffff;
      --bg-surface: #f8f7f6;
      --bg-card: #ffffff;
      --text-primary: #1a1a1a;
      --text-secondary: #666;
      --text-muted: #999;
      --border: #e5e3e0;
      --border-light: #d5d3d0;
      --success: #059669;
      --warning: #d97706;
    }

    [data-theme="dark"] {
      --primary: #2c5aa0;
      --secondary: #1a1a1a;
      --accent: #f0a000;
      --bg-dark: #0f0f0f;
      --bg-surface: #1a1a1a;
      --bg-card: #262626;
      --text-primary: #e8e8e8;
      --text-secondary: #b0b0b0;
      --text-muted: #707070;
      --border: #3a3a3a;
      --border-light: #4a4a4a;
      --success: #10b981;
      --warning: #f59e0b;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
      background: var(--bg-dark);
      color: var(--text-primary);
      line-height: 1.6;
      overflow-x: hidden;
      transition: background 0.3s ease, color 0.3s ease;
    }

    ::-webkit-scrollbar {
      width: 8px;
    }

    ::-webkit-scrollbar-track {
      background: var(--bg-surface);
    }

    ::-webkit-scrollbar-thumb {
      background: var(--border-light);
      border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: var(--primary);
    }

    .container {
      max-width: 1000px;
      margin: 0 auto;
      padding: 0 2rem;
    }

    /* Header */
    header {
      position: fixed;
      top: 0;
      right: 0;
      padding: 2rem;
      z-index: 100;
      display: flex;
      gap: 1rem;
      align-items: center;
    }

    .theme-toggle {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--bg-card);
      border: 1px solid var(--border);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      transition: all 0.3s ease;
      position: relative;
    }

    .theme-toggle:hover {
      border-color: var(--primary);
      transform: scale(1.1);
      box-shadow: 0 8px 24px rgba(44, 90, 160, 0.2);
    }

    .theme-toggle::before {
      content: "☀️";
      position: absolute;
      transition: all 0.3s ease;
      opacity: 1;
    }

    .theme-toggle.dark::before {
      opacity: 0;
      transform: rotate(180deg);
    }

    .theme-toggle.dark::after {
      content: "🌙";
      position: absolute;
      opacity: 1;
      transition: all 0.3s ease;
    }

    .theme-toggle::after {
      content: "🌙";
      opacity: 0;
      transform: rotate(180deg);
    }

    .github-stats {
      font-size: 12px;
      padding: 0.5rem 1rem;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 20px;
      color: var(--text-secondary);
      transition: all 0.3s ease;
    }

    .github-stats:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    /* Scroll indicator */
    .scroll-indicator {
      position: fixed;
      left: 0;
      top: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      width: 0%;
      z-index: 101;
      transition: width 0.1s ease;
    }

    /* Toast notifications */
    .toast-container {
      position: fixed;
      top: 80px;
      right: 2rem;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .toast {
      padding: 1rem 1.5rem;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      animation: slideInRight 0.4s ease-out;
      min-width: 300px;
      font-size: 14px;
    }

    .toast.success {
      border-left-color: var(--success);
    }

    .toast.error {
      border-left-color: #ef4444;
    }

    .toast.warning {
      border-left-color: var(--warning);
    }

    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateX(100px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    /* Modal */
    .modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      z-index: 999;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
    }

    .modal.active {
      display: flex;
      animation: fadeIn 0.3s ease-out;
    }

    .modal-content {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2rem;
      max-width: 500px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      animation: slideUp 0.3s ease-out;
    }

    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .modal-close {
      float: right;
      font-size: 24px;
      font-weight: bold;
      cursor: pointer;
      color: var(--text-muted);
      transition: color 0.3s ease;
    }

    .modal-close:hover {
      color: var(--primary);
    }

    .modal-header {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 1.5rem;
      font-size: 32px;
    }

    .modal-title {
      font-size: 20px;
      font-weight: 600;
      color: var(--text-primary);
      margin: 0;
    }

    .modal-subtitle {
      font-size: 14px;
      color: var(--primary);
      font-weight: 500;
      margin-bottom: 0.5rem;
    }

    .modal-body {
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.8;
      margin-bottom: 1.5rem;
    }

    .modal-buttons {
      display: flex;
      gap: 1rem;
    }

    .modal-btn {
      flex: 1;
      padding: 0.75rem 1.5rem;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--primary);
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.3s ease;
    }

    .modal-btn:hover {
      background: var(--bg-surface);
      border-color: var(--primary);
    }

    .modal-btn.primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }

    .modal-btn.primary:hover {
      opacity: 0.9;
    }

    /* Hero Section */
    .hero {
      min-height: 60vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      position: relative;
      overflow: hidden;
      padding: 4rem 0;
    }

    .hero::before {
      content: "";
      position: absolute;
      top: -50%;
      right: -20%;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(44, 90, 160, 0.15) 0%, transparent 70%);
      border-radius: 50%;
      z-index: 0;
      animation: float 6s ease-in-out infinite;
    }

    .hero::after {
      content: "";
      position: absolute;
      bottom: -30%;
      left: -10%;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(240, 160, 0, 0.1) 0%, transparent 70%);
      border-radius: 50%;
      z-index: 0;
      animation: float 8s ease-in-out infinite reverse;
    }

    .hero-content {
      position: relative;
      z-index: 1;
      max-width: 600px;
    }

    .hero h1 {
      font-size: 56px;
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 1.5rem;
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      letter-spacing: -1px;
      animation: fadeInUp 0.8s ease-out;
    }

    .hero p {
      font-size: 18px;
      color: var(--text-secondary);
      margin-bottom: 1rem;
      line-height: 1.7;
      animation: fadeInUp 0.8s ease-out 0.1s both;
    }

    .hero .tagline {
      font-size: 14px;
      color: var(--text-muted);
      font-style: italic;
      animation: fadeInUp 0.8s ease-out 0.2s both;
    }

    .section {
      margin: 6rem 0;
      opacity: 0;
      transition: opacity 0.8s ease-out;
    }

    .section.visible {
      opacity: 1;
      animation: fadeInUp 0.8s ease-out;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .section-title {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: var(--primary);
      position: relative;
      padding-bottom: 1rem;
    }

    .section-title::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      width: 40px;
      height: 3px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      border-radius: 2px;
      transform: scaleX(0);
      transform-origin: left;
      transition: transform 0.6s ease-out 0.2s;
    }

    .section.visible .section-title::after {
      transform: scaleX(1);
    }

    /* Filter buttons */
    .filter-buttons {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .filter-btn {
      padding: 0.5rem 1rem;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-secondary);
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.3s ease;
      font-weight: 500;
    }

    .filter-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }

    .filter-btn.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }

    .doing-list {
      display: grid;
      gap: 1.5rem;
    }

    .doing-item {
      padding: 1.5rem;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
      cursor: pointer;
      opacity: 0;
      transform: translateX(-20px);
    }

    .section.visible .doing-item {
      opacity: 1;
      transform: translateX(0);
      animation: slideInLeft 0.6s ease-out forwards;
    }

    .doing-item:nth-child(1) { animation-delay: 0.1s; }
    .doing-item:nth-child(2) { animation-delay: 0.2s; }
    .doing-item:nth-child(3) { animation-delay: 0.3s; }

    .doing-item::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, rgba(44, 90, 160, 0.05) 0%, transparent 100%);
      pointer-events: none;
    }

    .doing-item:hover {
      border-color: var(--primary);
      transform: translateX(4px);
      box-shadow: 0 8px 24px rgba(44, 90, 160, 0.15);
    }

    .doing-label {
      font-weight: 600;
      color: var(--primary);
      margin-right: 0.5rem;
      display: inline-block;
    }

    .doing-item p {
      position: relative;
      z-index: 1;
      font-size: 15px;
      line-height: 1.7;
    }

    .projects-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 2rem;
    }

    .project-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 2rem;
      transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      opacity: 0;
      transform: translateY(20px);
      cursor: pointer;
    }

    .section.visible .project-card {
      opacity: 1;
      transform: translateY(0);
      animation: slideInUp 0.6s ease-out forwards;
    }

    .project-card:nth-child(1) { animation-delay: 0.1s; }
    .project-card:nth-child(2) { animation-delay: 0.2s; }
    .project-card:nth-child(3) { animation-delay: 0.3s; }
    .project-card:nth-child(4) { animation-delay: 0.4s; }
    .project-card:nth-child(5) { animation-delay: 0.5s; }
    .project-card:nth-child(6) { animation-delay: 0.6s; }

    .project-card.hidden {
      display: none;
    }

    .project-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(135deg, rgba(44, 90, 160, 0.05) 0%, transparent 100%);
      opacity: 0;
      transition: opacity 0.4s ease;
      pointer-events: none;
    }

    .project-card::after {
      content: "";
      position: absolute;
      top: -2px;
      left: -2px;
      right: -2px;
      bottom: -2px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border-radius: 12px;
      z-index: -1;
      opacity: 0;
      transition: opacity 0.4s ease;
    }

    .project-card:hover {
      border-color: var(--primary);
      transform: translateY(-8px);
    }

    .project-card:hover::before {
      opacity: 1;
    }

    .project-icon {
      font-size: 32px;
      margin-bottom: 1rem;
      display: inline-block;
      transition: transform 0.3s ease;
    }

    .project-card:hover .project-icon {
      transform: scale(1.2) rotate(5deg);
    }

    .project-content {
      position: relative;
      z-index: 1;
      flex-grow: 1;
    }

    .project-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }

    .project-subtitle {
      font-size: 13px;
      color: var(--primary);
      font-weight: 500;
      margin-bottom: 1rem;
      opacity: 0.8;
    }

    .project-desc {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 1.5rem;
      line-height: 1.7;
    }

    .project-links {
      display: flex;
      gap: 1rem;
    }

    .project-link {
      font-size: 13px;
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.3s ease;
      position: relative;
      flex: 1;
      padding: 0.5rem;
      border-radius: 4px;
      border: 1px solid var(--border);
      justify-content: center;
    }

    .project-link::after {
      content: "→";
      transition: transform 0.3s ease;
    }

    .project-link:hover {
      color: var(--accent);
      border-color: var(--primary);
      background: rgba(44, 90, 160, 0.05);
    }

    .project-link:hover::after {
      transform: translateX(4px);
    }

    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(44, 90, 160, 0.4);
      transform: scale(0);
      animation: ripple-effect 0.6s ease-out;
      pointer-events: none;
    }

    @keyframes ripple-effect {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }

    .tech-section {
      margin-top: 4rem;
    }

    .tech-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
      gap: 1rem;
    }

    .tech-badge {
      background: linear-gradient(135deg, rgba(44, 90, 160, 0.1), rgba(240, 160, 0, 0.05));
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem 1rem;
      text-align: center;
      font-size: 13px;
      color: var(--text-primary);
      font-weight: 500;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      cursor: default;
      position: relative;
      overflow: hidden;
      opacity: 0;
      transform: scale(0.8);
    }

    .section.visible .tech-badge {
      opacity: 1;
      transform: scale(1);
      animation: scaleIn 0.4s ease-out forwards;
    }

    .tech-badge:nth-child(1) { animation-delay: 0.05s; }
    .tech-badge:nth-child(2) { animation-delay: 0.1s; }
    .tech-badge:nth-child(3) { animation-delay: 0.15s; }
    .tech-badge:nth-child(4) { animation-delay: 0.2s; }
    .tech-badge:nth-child(5) { animation-delay: 0.25s; }
    .tech-badge:nth-child(6) { animation-delay: 0.3s; }
    .tech-badge:nth-child(7) { animation-delay: 0.35s; }
    .tech-badge:nth-child(8) { animation-delay: 0.4s; }
    .tech-badge:nth-child(9) { animation-delay: 0.45s; }

    .tech-badge::before {
      content: "";
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      opacity: 0;
      transition: opacity 0.3s ease;
      z-index: -1;
    }

    .tech-badge:hover {
      border-color: var(--primary);
      transform: translateY(-4px);
      box-shadow: 0 12px 24px rgba(44, 90, 160, 0.2);
    }

    .tech-badge:hover::before {
      opacity: 0.1;
    }

    .footer {
      margin-top: 6rem;
      padding: 3rem 0;
      border-top: 1px solid var(--border);
      text-align: center;
      opacity: 0;
    }

    .footer.visible {
      opacity: 1;
      animation: fadeInUp 0.8s ease-out;
    }

    .footer-links {
      display: flex;
      gap: 2rem;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }

    .footer-links a {
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
      transition: all 0.3s ease;
      position: relative;
    }

    .footer-links a::after {
      content: "";
      position: absolute;
      bottom: -4px;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      transform: scaleX(0);
      transform-origin: left;
      transition: transform 0.3s ease;
    }

    .footer-links a:hover::after {
      transform: scaleX(1);
    }

    .footer p {
      font-size: 12px;
      color: var(--text-muted);
    }

    /* Animations */
    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideInLeft {
      from {
        opacity: 0;
        transform: translateX(-20px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateX(100px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes scaleIn {
      from {
        opacity: 0;
        transform: scale(0.8);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }

    @keyframes float {
      0%, 100% {
        transform: translateY(0px);
      }
      50% {
        transform: translateY(-20px);
      }
    }

    @media (max-width: 768px) {
      header {
        padding: 1rem;
        flex-direction: column;
        gap: 0.5rem;
      }

      .github-stats {
        display: none;
      }

      .hero {
        min-height: 50vh;
        padding: 3rem 0;
      }

      .hero h1 {
        font-size: 40px;
      }

      .hero p {
        font-size: 16px;
      }

      .section-header {
        flex-direction: column;
        align-items: flex-start;
      }

      .filter-buttons {
        width: 100%;
      }

      .projects-grid {
        grid-template-columns: 1fr;
      }

      .tech-grid {
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
      }

      .footer-links {
        gap: 1rem;
      }

      .modal-content {
        width: 95%;
      }

      .toast-container {
        right: 1rem;
        left: 1rem;
      }

      .toast {
        min-width: auto;
      }
    }
  </style>
</head>
<body>
  <div class="scroll-indicator" id="scrollIndicator"></div>
  <div class="toast-container" id="toastContainer"></div>

  <header>
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme"></button>
    <div class="github-stats" id="githubStats">Loading...</div>
  </header>

  <!-- Modal -->
  <div class="modal" id="projectModal">
    <div class="modal-content">
      <span class="modal-close" id="modalClose">&times;</span>
      <div class="modal-header">
        <span id="modalIcon">🐳</span>
        <div>
          <div class="modal-title" id="modalTitle">Project Title</div>
          <div class="modal-subtitle" id="modalSubtitle">project_name</div>
        </div>
      </div>
      <div class="modal-body" id="modalBody">Project description</div>
      <div class="modal-buttons">
        <a href="#" class="modal-btn primary" id="modalGithubBtn" target="_blank">Visit GitHub</a>
        <button class="modal-btn" id="modalCloseBtn">Close</button>
      </div>
    </div>
  </div>

  <div class="container">
    <section class="hero">
      <div class="hero-content">
        <h1>Giovani Rodrigo</h1>
        <p>Developer building automation tools, DevOps solutions, and data extraction systems.</p>
        <p class="tagline">📍 Based in Natal, RN, Brazil</p>
      </div>
    </section>

    <section class="section" id="section-doing">
      <h2 class="section-title">What I'm Doing</h2>
      <div class="doing-list">
        <div class="doing-item">
          <p><span class="doing-label">Focus:</span> Python, Shell scripting, and infrastructure automation</p>
        </div>
        <div class="doing-item">
          <p><span class="doing-label">Interests:</span> Docker containerization, web scraping, Azure integrations</p>
        </div>
        <div class="doing-item">
          <p><span class="doing-label">Currently:</span> Expanding DevOps tooling and system utilities</p>
        </div>
      </div>
    </section>

    <section class="section" id="section-projects">
      <div class="section-header">
        <h2 class="section-title">Projects</h2>
        <div class="filter-buttons" id="filterButtons"></div>
      </div>
      <div class="projects-grid" id="projectsGrid"></div>
    </section>

    <section class="section" id="section-tech">
      <h2 class="section-title">Tech Stack</h2>
      <div class="tech-grid">
        <div class="tech-badge">Python</div>
        <div class="tech-badge">JavaScript</div>
        <div class="tech-badge">TypeScript</div>
        <div class="tech-badge">C</div>
        <div class="tech-badge">Shell/Bash</div>
        <div class="tech-badge">PHP</div>
        <div class="tech-badge">Docker</div>
        <div class="tech-badge">Azure</div>
        <div class="tech-badge">Git</div>
      </div>
    </section>

    <footer class="footer" id="footer">
      <div class="footer-links">
        <a href="https://github.com/GiovaniRodrigo">GitHub</a>
        <a href="https://www.linkedin.com/in/giovani-fernandes-3a6384138/">LinkedIn</a>
      </div>
      <p>© 2026 Giovani Rodrigo. All rights reserved.</p>
    </footer>
  </div>

  <script>
    // =====================
    // PROJECTS DATA
    // =====================
    const projectsData = [
      {
        icon: '🐳',
        title: 'Dockerfile Generator',
        subtitle: 'gerador_dockerfile_php',
        description: 'Python tool to generate customized Dockerfiles for PHP (versions 5.6–8.2). Simplifies container setup for different PHP stacks.',
        github: 'https://github.com/GiovaniRodrigo/gerador_dockerfile_php',
        tags: ['Python', 'Docker']
      },
      {
        icon: '🔗',
        title: 'URL Shortener',
        subtitle: 'shorter_url',
        description: 'Lightweight application for URL shortening and management. Fast, reliable, and easy to integrate.',
        github: 'https://github.com/GiovaniRodrigo/shorter_url',
        tags: ['JavaScript']
      },
      {
        icon: '🕷️',
        title: 'Web Scraping',
        subtitle: 'web_scraping',
        description: 'Data extraction and analysis from web sources. Built for reliable scraping workflows with error handling.',
        github: 'https://github.com/GiovaniRodrigo/web_scraping',
        tags: ['Python']
      },
      {
        icon: '☁️',
        title: 'Azure Automation',
        subtitle: 'azure_tasks',
        description: 'Integration and automation tools for Azure platform. Task scheduling and cloud operations made simple.',
        github: 'https://github.com/GiovaniRodrigo/azure_tasks',
        tags: ['Python', 'Azure']
      },
      {
        icon: '🔐',
        title: 'Certificate Validation',
        subtitle: 'validar_dependencias_token_certisign',
        description: 'C utility for validating Certisign token dependencies and certificate requirements. Security-focused.',
        github: 'https://github.com/GiovaniRodrigo/validar_dependencias_token_certisign',
        tags: ['C']
      },
      {
        icon: '🔧',
        title: 'Git Scripts',
        subtitle: 'git-scripts',
        description: 'Shell/Bash utilities to optimize Git workflows. Automate common operations and improve development speed.',
        github: 'https://github.com/GiovaniRodrigo/git-scripts',
        tags: ['Shell/Bash']
      }
    ];

    // =====================
    // THEME TOGGLE
    // =====================
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    const currentTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', currentTheme);
    updateThemeButton();

    themeToggle.addEventListener('click', () => {
      const newTheme = htmlElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      htmlElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeButton();
      showToast('Theme changed', 'success');
    });

    function updateThemeButton() {
      const isDark = htmlElement.getAttribute('data-theme') === 'dark';
      themeToggle.classList.toggle('dark', isDark);
    }

    // =====================
    // SCROLL INDICATOR
    // =====================
    const scrollIndicator = document.getElementById('scrollIndicator');
    window.addEventListener('scroll', () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollProgress = (window.scrollY / scrollHeight) * 100;
      scrollIndicator.style.width = scrollProgress + '%';
    });

    // =====================
    // INTERSECTION OBSERVER
    // =====================
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, observerOptions);

    document.querySelectorAll('.section, .footer').forEach(section => {
      observer.observe(section);
    });

    // =====================
    // TOAST NOTIFICATIONS
    // =====================
    function showToast(message, type = 'info') {
      const container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.textContent = message;
      container.appendChild(toast);

      setTimeout(() => {
        toast.style.animation = 'fadeInUp 0.4s ease-out reverse';
        setTimeout(() => toast.remove(), 400);
      }, 2500);
    }

    // =====================
    // MODAL
    // =====================
    const modal = document.getElementById('projectModal');
    const modalClose = document.getElementById('modalClose');
    const modalCloseBtn = document.getElementById('modalCloseBtn');

    modalClose.addEventListener('click', () => {
      modal.classList.remove('active');
    });

    modalCloseBtn.addEventListener('click', () => {
      modal.classList.remove('active');
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });

    function openProjectModal(project) {
      document.getElementById('modalIcon').textContent = project.icon;
      document.getElementById('modalTitle').textContent = project.title;
      document.getElementById('modalSubtitle').textContent = project.subtitle;
      document.getElementById('modalBody').textContent = project.description;
      document.getElementById('modalGithubBtn').href = project.github;
      modal.classList.add('active');
    }

    // =====================
    // PROJECTS RENDERING
    // =====================
    function renderProjects(filter = 'All') {
      const projectsGrid = document.getElementById('projectsGrid');
      projectsGrid.innerHTML = '';

      const filtered = filter === 'All' 
        ? projectsData 
        : projectsData.filter(p => p.tags.includes(filter));

      filtered.forEach((project, index) => {
        const card = document.createElement('div');
        card.className = 'project-card';
        card.innerHTML = `
          <div class="project-icon">${project.icon}</div>
          <div class="project-content">
            <div class="project-title">${project.title}</div>
            <div class="project-subtitle">${project.subtitle}</div>
            <div class="project-desc">${project.description}</div>
            <div class="project-links">
              <a href="${project.github}" class="project-link" target="_blank">GitHub</a>
              <button class="project-link" onclick="openProjectModal(projectsData[${index}])">Details</button>
            </div>
          </div>
        `;
        projectsGrid.appendChild(card);
      });

      // Re-observe new cards
      document.querySelectorAll('.project-card').forEach(card => {
        observer.observe(card);
      });
    }

    // =====================
    // FILTER BUTTONS
    // =====================
    function renderFilterButtons() {
      const filterContainer = document.getElementById('filterButtons');
      const tags = ['All', ...new Set(projectsData.flatMap(p => p.tags))];

      tags.forEach(tag => {
        const btn = document.createElement('button');
        btn.className = `filter-btn ${tag === 'All' ? 'active' : ''}`;
        btn.textContent = tag;
        btn.addEventListener('click', () => {
          document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          renderProjects(tag);
          showToast(`Filtering by ${tag}`, 'info');
        });
        filterContainer.appendChild(btn);
      });
    }

    renderFilterButtons();
    renderProjects();

    // =====================
    // GITHUB STATS
    // =====================
    async function fetchGithubStats() {
      try {
        const response = await fetch('https://api.github.com/users/GiovaniRodrigo');
        const data = await response.json();
        const statsEl = document.getElementById('githubStats');
        statsEl.innerHTML = `⭐ ${data.public_repos} repos · 👥 ${data.followers} followers`;
        statsEl.style.cursor = 'pointer';
        statsEl.addEventListener('click', () => {
          window.open('https://github.com/GiovaniRodrigo', '_blank');
        });
      } catch (error) {
        console.error('Error fetching GitHub stats:', error);
        document.getElementById('githubStats').textContent = '📊 GitHub Stats';
      }
    }

    fetchGithubStats();

    // =====================
    // PARALLAX EFFECT
    // =====================
    const hero = document.querySelector('.hero');
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      hero.style.transform = `translateY(${scrollY * 0.5}px)`;
    });

    // =====================
    // RIPPLE EFFECT
    // =====================
    document.addEventListener('click', function(e) {
      if (e.target.closest('.project-card') || e.target.closest('.doing-item')) {
        const element = e.target.closest('.project-card') || e.target.closest('.doing-item');
        const ripple = document.createElement('div');
        ripple.classList.add('ripple');
        
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
      }
    });

    // =====================
    // KEYBOARD SHORTCUTS
    // =====================
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        modal.classList.remove('active');
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        showToast('Search coming soon!', 'warning');
      }
    });

    // =====================
    // PAGE LOAD ANIMATION
    // =====================
    window.addEventListener('load', () => {
      showToast('Welcome! 👋', 'success');
    });

    // =====================
    // CONSOLE EASTER EGG
    // =====================
    console.log('%c👋 Olá, developer!', 'font-size: 24px; font-weight: bold; color: #2c5aa0;');
    console.log('%cFique à vontade para explorar o código-fonte', 'font-size: 14px; color: #f0a000;');
    console.log('%cGitHub: github.com/GiovaniRodrigo', 'font-size: 12px; color: #b0b0b0;');
    console.log('%cTip: Press Ctrl+K to search (coming soon)', 'font-size: 12px; color: #10b981;');
  </script>
</body>
</html>
