\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ucrnotes}[2026/07/20 UCR Notes]

%----------------------------------------
% Clase base
%----------------------------------------

\LoadClass[12pt]{article}

%----------------------------------------
% Paquetes
%----------------------------------------

\RequirePackage{fontspec}
\RequirePackage{libertinus}

\RequirePackage[
a4paper,
left=3cm,
right=3cm,
top=2.8cm,
bottom=2.8cm
]{geometry}
\setlength{\headheight}{15pt}

\RequirePackage{setspace}
\setstretch{1.15}

\RequirePackage{fancyhdr}
\RequirePackage{lastpage}

%----------------------------------------
% Metadata
%----------------------------------------

\newcommand{\course}[1]{\def\ucrcourse{#1}}
\newcommand{\doctitle}[1]{\def\ucrdoctitle{#1}}
\renewcommand{\author}[1]{\def\ucrauthor{#1}}
\newcommand{\documentdate}[1]{\def\ucrdate{#1}}

\course{}
\doctitle{}
\author{Ignacio Sanabria}
\documentdate{\today}

%----------------------------------------
% Layout
%----------------------------------------

\pagestyle{fancy}
\fancyhf{}

\fancyhead[R]{\ucrdoctitle}
\fancyfoot[C]{\thepage}

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

%----------------------------------------
% Portada
%----------------------------------------

\newcommand{\maketitlepage}{

\begin{titlepage}

\thispagestyle{empty}

\vspace*{\fill}

\begin{center}

{\Huge\bfseries \ucrcourse}

\vspace{1cm}

{\Large \ucrdoctitle}

\vspace{2.5cm}

{\large \ucrauthor}

\vspace{3cm}

Actualizado

\vspace{0.3cm}

\ucrdate

\end{center}

\vspace*{\fill}

\end{titlepage}

\clearpage

}