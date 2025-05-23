const COOKIE_NAME = 'show_hidden_games';

function setCookie(name, value, days = 365) {
  const expires = new Date(Date.now() + days*864e5).toUTCString();
  document.cookie = `${name}=${value};expires=${expires};path=/`;
}

function getCookie(name) {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='))
    ?.split('=')[1];
}

const showError = () => {
  const tutorial = document.getElementById('tutorial-landing');
  document.getElementById('page-title').innerText = 'This page is out of logic!';
  tutorial.removeChild(document.getElementById('loading'));
  const userMessage = document.createElement('h3');
  const homepageLink = document.createElement('a');
  homepageLink.innerText = 'Click here';
  homepageLink.setAttribute('href', '/');
  userMessage.append(homepageLink);
  userMessage.append(' to go back to safety!');
  tutorial.append(userMessage);
};

window.addEventListener('load', () => {
    const toggleLink = document.getElementById('toggle-nsfw');
    toggleLink.addEventListener('click', e => {
      e.preventDefault();
      const currently = getCookie(COOKIE_NAME) === 'true';
      setCookie(COOKIE_NAME, !currently);
      // simple reload to reapply filter
      window.location.reload();
    });
  
    const isShowing = getCookie(COOKIE_NAME) === 'true';
    toggleLink.textContent = isShowing
      ? 'Hide NSFW games'
      : 'Show NSFW games';

  const ajax = new XMLHttpRequest();
  ajax.onreadystatechange = () => {
    if (ajax.readyState !== 4) { return; }
    const tutorialDiv = document.getElementById('tutorial-landing');
    if (ajax.status !== 200) { return showError(); }

    try {
      const games = JSON.parse(ajax.responseText);

      const showAll = getCookie(COOKIE_NAME) === 'true';
      const visibleGames = games.filter(game =>
        showAll || !game.rating?.toLowerCase().includes('nsfw')
      );

      visibleGames.forEach((game) => {
          if ("tutorials" in game) {
              const gameTitle = document.createElement('h2');
              gameTitle.innerText = game.gameTitle;
              gameTitle.id = `${encodeURIComponent(game.gameTitle)}`;
              tutorialDiv.appendChild(gameTitle);
              game.tutorials.forEach((tutorial) => {
                  const tutorialName = document.createElement('h3');
                  tutorialName.innerText = tutorial.name;
                  tutorialDiv.appendChild(tutorialName);

                  const tutorialDescription = document.createElement('p');
                  tutorialDescription.innerText = tutorial.description;
                  tutorialDiv.appendChild(tutorialDescription);

                  const intro = document.createElement('p');
                  intro.innerText = 'This guide is available in the following languages:';
                  tutorialDiv.appendChild(intro);

                  const fileList = document.createElement('ul');
                  tutorial.files.forEach((file) => {
                      const listItem = document.createElement('li');
                      const anchor = document.createElement('a');
                      anchor.innerText = file.language;
                      anchor.setAttribute('href', `${window.location.origin}/tutorial/${file.link}`);
                      listItem.appendChild(anchor);

                      listItem.append(' by ');
                      for (let author of file.authors) {
                          listItem.append(author);
                          if (file.authors.indexOf(author) !== (file.authors.length -1)) {
                              listItem.append(', ');
                          }
                      }

                      fileList.appendChild(listItem);
                  });
                  tutorialDiv.appendChild(fileList);
              });
          }
      });

      tutorialDiv.removeChild(document.getElementById('loading'));
    } catch (error) {
      showError();
      console.error(error);
    }

    // Check if we are on an anchor when coming in, and scroll to it.
    const hash = window.location.hash;
    if (hash) {
      const offset = 128;  // To account for navbar banner at top of page.
      window.scrollTo(0, 0);
      const rect = document.getElementById(hash.slice(1)).getBoundingClientRect();
      window.scrollTo(rect.left, rect.top - offset);
    }
  };
  ajax.open('GET', `${window.location.origin}/static/generated/tutorials.json`, true);
  ajax.send();
});
