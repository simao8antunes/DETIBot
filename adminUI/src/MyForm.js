import React, { useState } from 'react';
import { Form, Button, Card, Row, Col } from 'react-bootstrap';
import axios from 'axios';

const MyForm = () => {
  const [sourceType, setSourceType] = useState('');
  const [file, setFile] = useState(null); // Using null instead of empty string for file
  const [url, setUrl] = useState('');
  const [description, setDescription] = useState('');
  const [frequency, setFrequency] = useState('');
  const [recursive, setRecursive] = useState(false);
  const [pathsEnabled, setPathsEnabled] = useState(false);
  const [paths, setPaths] = useState([]);

  const handleSourceTypeChange = (event) => {
    setSourceType(event.target.value);
    // Reset paths and other related state when changing source type
    setPathsEnabled(false);
    setPaths([]);
    setRecursive(false);
    // Reset file and url inputs
    setFile(null);
    setUrl('');
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Set the file object directly
  };

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleFrequencyChange = (event) => {
    setFrequency(event.target.value);
  };

  const handleRecursiveChange = () => {
    setRecursive(!recursive);
  };

  const handlePathsEnabledChange = () => {
    setPathsEnabled(!pathsEnabled);
  };

  const handlePathChange = (event, index) => {
    const newPaths = [...paths];
    newPaths[index] = event.target.value;
    setPaths(newPaths);
  };

  const handleAddPath = () => {
    setPaths([...paths, '']);
  };

  const handleRemovePath = (index) => {
    const newPaths = [...paths];
    newPaths.splice(index, 1);
    setPaths(newPaths);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    // Prepare data for the API call
    const data = {
      url: sourceType === 'url' ? url : '',
      paths: pathsEnabled ? paths : [],
      loader_type: sourceType === 'file' ? 'file' : 'url',
      update_period: frequency,
      description: description,
      wait_time: 3,
      recursive: recursive
    };

    let apiUrl = '';
    if (sourceType === 'url') {
      apiUrl = 'http://localhost:8000/detibot/insert_urlsource';
    } else if (sourceType === 'file') {
      apiUrl = 'http://localhost:8000/detibot/insert_filesource';
    }

    try {
      // Make the POST request using Axios
      const response = await axios.post(apiUrl, data, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
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

            <Form.Group controlId="sourceValue">
              <Form.Label>{sourceType === 'file' ? 'Upload File:' : 'URL:'}</Form.Label>
              {sourceType === 'file' ? (
                <Form.Control
                  type="file"
                  onChange={handleFileChange}
                  style={{ color: '#1e90ff' }}
                />
              ) : (
                <Form.Control
                  type="text"
                  placeholder={sourceType === 'file' ? 'Choose file' : 'Enter URL'}
                  value={url}
                  onChange={handleUrlChange}
                  style={{ color: '#1e90ff' }}
                />
              )}
            </Form.Group>

            {sourceType === 'url' && (
              <>
                <Form.Group controlId="recursive">
                  <Form.Check
                    type="checkbox"
                    label="Recursive"
                    checked={recursive}
                    onChange={handleRecursiveChange}
                    style={{ marginLeft: '10px', color: '#1e90ff' }}
                  />
                </Form.Group>
                <Form.Group controlId="pathsEnabled">
                  <Form.Check
                    type="switch"
                    label="Enable Paths"
                    checked={pathsEnabled}
                    onChange={handlePathsEnabledChange}
                    style={{ marginLeft: '10px', color: '#1e90ff' }}
                  />
                </Form.Group>
                {pathsEnabled && (
                  <>
                    {paths.map((path, index) => (
                      <Row key={index} className="mb-2">
                        <Col>
                          <Form.Control
                            type="text"
                            placeholder="Enter path"
                            value={path}
                            onChange={(event) => handlePathChange(event, index)}
                            style={{ color: '#1e90ff' }}
                          />
                        </Col>
                        <Col xs="auto">
                          <Button variant="danger" onClick={() => handleRemovePath(index)}>Remove</Button>
                        </Col>
                      </Row>
                    ))}
                    <Button variant="primary" onClick={handleAddPath}>Add Path</Button>
                  </>
                )}
              </>
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
