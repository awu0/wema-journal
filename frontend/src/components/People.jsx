import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BACKEND_URL } from '../../constants';

const PEOPLE_READ_ENDPOINT = `${BACKEND_URL}/people`;

function AddPersonForm({ visible, cancel, fetchPeople, setError }) {
    if (!visible) return null;
    return (
        <div>
            <h2>Add a Person</h2>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}

function ErrorMessage({ message }) {
    return <div className="error">{message}</div>;
}

function Person({ person }) {
    return <div>{person.name}</div>;
}

function peopleObjectToArray(data) {
    return Object.values(data); // Convert object to an array
}

function People() {
    const [error, setError] = useState(''); // For error messages
    const [people, setPeople] = useState([]); // For people data
    const [addingPerson, setAddingPerson] = useState(false); // To show/hide the form

    const fetchPeople = () => {
        axios.get(PEOPLE_READ_ENDPOINT)
            .then(({ data }) => {
                setPeople(peopleObjectToArray(data));
            })
            .catch((err) => {
                setError(`There was a problem retrieving the list of people. ${err.message}`);
            });
    };

    const showAddPersonForm = () => setAddingPerson(true);
    const hideAddPersonForm = () => setAddingPerson(false);

    useEffect(() => {
        fetchPeople();
    }, []);

    return (
        <div className="wrapper">
            <header>
                <h1>View All People</h1>
                <button type="button" onClick={showAddPersonForm}>
                    Add a Person
                </button>
            </header>
            <AddPersonForm
                visible={addingPerson}
                cancel={hideAddPersonForm}
                fetchPeople={fetchPeople}
                setError={setError}
            />
            {error && <ErrorMessage message={error} />}
            {people.map((person) => (
                <Person key={person.name} person={person} />
            ))}
        </div>
    );
}

export default People;
