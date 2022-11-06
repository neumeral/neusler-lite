import React from 'react'
import ReactDOM from 'react-dom/client'
import Poll from './polls/Poll'

document.querySelectorAll('.poll_container')
  .forEach(domContainer => {
    const questionId = parseInt(domContainer.dataset.pollquestionid, 10);
    const root = ReactDOM.createRoot(domContainer);
    root.render(
        <Poll questionId={questionId} />
    );
  });