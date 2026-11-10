/* Videos embedded through the local video_figure extension are rendered without
   native playback controls so they look and behave like the animated GIFs they
   replace. Click, Space or Enter toggles play/pause, and videos pause while
   scrolled out of view so a page with several animations does not decode them
   all at once. */

(() => {
  const play = (video) => {
    const started = video.play();
    if (started) {
      started.catch(() => {
        /* Autoplay may be blocked; the click/keyboard handler can retry. */
      });
    }
  };

  const toggle = (video) => {
    if (video.paused) {
      play(video);
    } else {
      video.pause();
    }
  };

  const init = () => {
    const videos = document.querySelectorAll("figure video.book-video");
    if (videos.length === 0) {
      return;
    }

    videos.forEach((video) => {
      video.tabIndex = 0;
      video.addEventListener("click", () => toggle(video));
      video.addEventListener("keydown", (event) => {
        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          toggle(video);
        }
      });
    });

    if (!("IntersectionObserver" in window)) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            play(entry.target);
          } else {
            entry.target.pause();
          }
        });
      },
      { threshold: 0.1 }
    );
    videos.forEach((video) => observer.observe(video));
  };

  // html_js_files are loaded in <head>, before the body is parsed.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
