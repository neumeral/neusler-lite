import { useState, useEffect } from 'react'
import { getPoll } from './api';


function Poll({ questionId }) {
  const [question, setQuestion] = useState('');
  const [pollOptions, setPollOptions] = useState([]);

  const defaultOptions = [
    {
      "id": 1,
      "option": "Yes",
      "votes": 10
    },
    {
      "id": 1,
      "option": "No",
      "votes": 12
    }
  ];

  useEffect(() => {
   let mounted = true;

   getPoll(questionId)
     .then(poll => {
       if(mounted) {
         setQuestion(poll.title);
         setPollOptions(defaultOptions);
       }
     })
   return () => mounted = false;
  }, [])

  return (
    <div className="poll-wrap my-3 p-2 border border-2 border-info rounded rounded-2 bg-light">
      <h5>{question}</h5>
      <p>This is the container for poll - {questionId}</p>

      <div className='row'>

        { pollOptions.map(item => (
          <div className='col-6' key={`${questionId}-${item.id}`}>
            <button className='btn btn-block btn-outline-info w-100' data-option_id={item.id}>{item.option}</button>
            <div className='px-1 mt-2'><span className='small badge text-bg-info'>{`${item.votes} votes`}</span></div>
          </div> 
        ))}
        
        
      </div>

    </div>
  )
}

export default Poll
