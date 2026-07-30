\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ucrnotes[2026/07/20 UCR Notes]}

% Clase base
\LoadClass[11pt]{article}

% ------------------------
% Paquetes
% ------------------------

\RequirePackage{fontspec}
\RequirePackage{libertinus}

\RequirePackage[a4paper,
left=3cm,
right=3cm,
top=2.8cm,
bottom=2.8cm]{geometry}

\RequirePackage{setspace}
\setstretch{1.15}

\RequirePackage{fancyhdr}
\RequirePackage{lastpage}

% ------------------------
% Archivos propios
% ------------------------

\input{commands}
\input{layout}
\input{titlepage}