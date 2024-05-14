import React, { useState } from 'react';
import { Form, Button, Card } from 'react-bootstrap';
import axios from 'axios';

const MyForm = () => {
  const [sourceType, setSourceType] = useState('');
  const [sourceValue, setSourceValue] = useState('');
  const [description, setDescription] = useState('');
  const [frequency, setFrequency] = useState('');

  const handleSourceTypeChange = (event) => {
    setSourceType(event.target.value);
  };

  const handleSourceValueChange = (event) => {
    setSourceValue(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleFrequencyChange = (event) => {
    setFrequency(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Prepare data for the API call
    const data = {
      url: sourceType === 'url' ? sourceValue : '',
      paths: [],
      loader_type: sourceType === 'file' ? 'file' : 'email',
      update_period: frequency,
      description: description,
      wait_time: 3,
      recursive: false
    };

    try {
      // Make the POST request
      const response = await axios.post('detibot/insert_source', data);
      console.log('API response:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <>
      <h2 className="text-center mb-4" style={{ fontFamily: 'Poppins, sans-serif', color: '#666', fontWeight: 'lighter', letterSpacing: '1px', lineHeight: '1.5', borderRadius: '10px', fontSize: '28px' }}>Loader</h2>
      <Card className="shadow p-3 mb-5 bg-white rounded" style={{ borderRadius: '30px', padding: '20px', maxWidth: '600px', width: 'auto', margin: '20px auto', border: '2px solid #1e90ff' }}>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="sourceType">
              <Form.Label>Type of Source:</Form.Label>
              <div>
                <Form.Check
                  type="radio"
                  label="Email"
                  value="email"
                  checked={sourceType === 'email'}
                  onChange={handleSourceTypeChange}
                  style={{ marginLeft: '10px', color: '#1e90ff' }}
                />
                <Form.Check
                  type="radio"
                  label="File"
                  value="file"
                  checked={sourceType === 'file'}
                  onChange={handleSourceTypeChange}
                  style={{ marginLeft: '10px', color: '#1e90ff' }}
                />
                <Form.Check
                  type="radio"
                  label="URL"
                  value="url"
                  checked={sourceType === 'url'}
                  onChange={handleSourceTypeChange}
                  style={{ marginLeft: '10px', color: '#1e90ff' }}
                />
              </div>
            </Form.Group>

            {sourceType === 'file' && (
              <Form.Group controlId="file">
                <Form.Label>Upload File:</Form.Label>
                <Form.Control
                  type="file"
                  onChange={handleSourceValueChange}
                  style={{ color: '#1e90ff' }}
                />
              </Form.Group>
            )}

            {sourceType !== 'file' && (
              <Form.Group controlId="sourceValue">
                <Form.Label>{sourceType === 'email' ? 'Email Address:' : 'URL:'}</Form.Label>
                <Form.Control
                  type={sourceType === 'email' ? 'email' : 'text'}
                  placeholder={sourceType === 'email' ? 'Enter email address' : 'Enter URL'}
                  value={sourceValue}
                  onChange={handleSourceValueChange}
                  style={{ color: '#1e90ff' }}
                />
              </Form.Group>
            )}

            <Form.Group controlId="description">
              <Form.Label>Description:</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={description}
                onChange={handleDescriptionChange}
                style={{ borderRadius: '10px', color: '#1e90ff' }}
              />
            </Form.Group>

            <Form.Group controlId="frequency">
              <Form.Label>Frequency of Updates:</Form.Label>
              <Form.Control
                as="select"
                value={frequency}
                onChange={handleFrequencyChange}
                style={{ borderRadius: '10px', color: '#1e90ff' }}
              >
                <option value="">Select Frequency</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="quarterly">Quarterly</option>
              </Form.Control>
            </Form.Group>

            <br />

            <Button variant="primary" type="submit" style={{ borderRadius: '10px', backgroundColor: '#1e90ff', border: 'none' }}>
              Submit
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </>
  );
};

export default MyForm;
