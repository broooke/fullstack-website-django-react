import React, {useState, setState} from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom'

function SearchBox() {
	const [keyword, setKeyword] = useState('')

	let history = useHistory()

	const submitHandler = (e) => {
		e.preventDefault()
		if(keyword){
			history.push(`/?keyword=${keyword}&page=1`)
			// const a = document.getElementById('search').value=''
		}else{
			history.push(history.push(history.location.pathname))
		}
	}

	return (
		<Form onSubmit={submitHandler} inline>
			<Form.Control
				type='text'
				id='search'
				name='q'
				onChange={(e)=>setKeyword(e.target.value)}
				className='mr-sm-2 ml-sm-5'
			>
			</Form.Control>
			<Button
				type='submit'
				variant='outline-light'
				className='p-2'
			>
				Submit
			</Button>
		</Form>
	)
}

export default SearchBox