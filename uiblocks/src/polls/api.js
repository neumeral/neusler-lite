function getCSRFToken(){
  const tokenElement = document.getElementById('#poll-csrftoken');
  let csrftoken = '';

  if(tokenElement){
    csrftoken = tokenElement.dataset.value; 
  }
  
  return csrftoken;
}

export function getPoll(questionId) {

  let data = new FormData();
  data.append('file', 'a');
  data.append('fileName', 'b');

  const csrftoken = getCSRFToken();
  data.append('csrfmiddlewaretoken', csrftoken);

  return fetch(`https://jsonplaceholder.typicode.com/posts/${questionId}`, {
      method: 'GET',
      // body: data,
      credentials: 'same-origin',
  }).then(data => data.json());

}
