import React, { useState, useEffect } from 'react';
import { Table, Button, Form, FormControl, Container, Row, Col, Card } from 'react-bootstrap';
import axios from 'axios';
import './App.css'; // Import the custom CSS file

const App = () => {
  const [urlSources, setUrlSources] = useState([]);
  const [fileSources, setFileSources] = useState([]);
  const [faqSources, setFaqSources] = useState([]);
  const [searchUrl, setSearchUrl] = useState('');
  const [searchFile, setSearchFile] = useState('');
  const [searchFaq, setSearchFaq] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const urlResponse = await axios.get('http://localhost:8000/detibot/url_sources');
      const fileResponse = await axios.get('http://localhost:8000/detibot/file_sources');
      const faqResponse = await axios.get('http://localhost:8000/detibot/faq_sources');
      console.log(faqResponse.data)
      setUrlSources(urlResponse.data);
      setFileSources(fileResponse.data);
      setFaqSources(faqResponse.data);
    } catch (error) {
      console.error('Error fetching data', error);
    }
  };

  const deleteEntry = async (type, id) => {
    const endpoints = {
      url: `http://localhost:8000/detibot/delete_urlsource/${id}`,
      file: `http://localhost:8000/detibot/delete_filesource/${id}`,
      faq: `http://localhost:8000/detibot/delete_faqsource/${id}`,
    };

    try {
      await axios.delete(endpoints[type]);
      fetchData();
    } catch (error) {
      console.error('Error deleting entry', error);
    }
  };

  const searchEntries = async (type, query) => {
    const endpoints = {
      url: `http://localhost:8000/detibot/Search_url_sources/${query}`,
      file: `http://localhost:8000/detibot/Search_file_sources/${query}`,
      faq: `http://localhost:8000/detibot/Search_faq_sources/${query}`,
    };

    try {
      const response = await axios.get(endpoints[type]);
      if (type === 'url') setUrlSources(response.data);
      if (type === 'file') setFileSources(response.data);
      if (type === 'faq') setFaqSources(response.data);
    } catch (error) {
      console.error('Error searching entries', error);
    }
  };

  return (
    <Container>
      <div className="page-title-container">
        <h1 className="page-title">Sources Manager</h1>
        <Button variant="primary" href="http://localhost:3010" className="add-entry-button">Add Entry</Button>
      </div>

      <Card className="shadow-sm mb-4">
        <Card.Body>
          <Row className="my-3">
            <Col>
              <h2 className="table-title">URL Sources</h2>
              <Form className="d-flex mb-3 search-bar">
                <FormControl
                  type="search"
                  placeholder="Search"
                  className="me-2"
                  value={searchUrl}
                  onChange={(e) => setSearchUrl(e.target.value)}
                />
                <Button variant="outline-success" onClick={() => searchEntries('url', searchUrl)}>Search</Button>
              </Form>
              <div className="table-wrapper">
                <Table responsive striped hover className="table-sm">
                  <thead className="thead-light">
                    <tr>
                      <th className="id-column">ID</th>
                      <th className="url-column">URL</th>
                      <th className="paths-column">Paths</th>
                      <th className="update-period-column">Update Period</th>
                      <th className="description-column">Description</th>
                      <th className="recursive-column">Recursive</th>
                      <th className="action-column">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {urlSources.map((source) => (
                      <tr key={source.id}>
                        <td className="id-column">{source.id}</td>
                        <td className="url-column">{source.url}</td>
                        <td className="paths-column">{source.paths.join(', ')}</td>
                        <td className="update-period-column">{source.update_period}</td>
                        <td className="description-column">{source.description}</td>
                        <td className="recursive-column">{source.recursive ? 'Yes' : 'No'}</td>
                        <td className="action-column">
                          <Button variant="danger" size="sm" onClick={() => deleteEntry('url', source.id)}>Delete</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Col>
          </Row>

          <Row className="my-3">
            <Col>
              <h2 className="table-title">File Sources</h2>
              <Form className="d-flex mb-3 search-bar">
                <FormControl
                  type="search"
                  placeholder="Search"
                  className="me-2"
                  value={searchFile}
                  onChange={(e) => setSearchFile(e.target.value)}
                />
                <Button variant="outline-success" onClick={() => searchEntries('file', searchFile)}>Search</Button>
              </Form>
              <div className="table-wrapper">
                <Table responsive striped hover className="table-sm">
                  <thead className="thead-light">
                    <tr>
                      <th className="id-column">ID</th>
                      <th className="file-name-column">File Name</th>
                      <th className="file-path-column">File Path</th>
                      <th className="file-description-column">Description</th>
                      <th className="action-column">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {fileSources.map((source) => (
                      <tr key={source.id}>
                        <td className="id-column">{source.id}</td>
                        <td className="file-name-column">{source.file_name}</td>
                        <td className="file-path-column">{source.file_path}</td>
                        <td className="file-description-column">{source.description}</td>
                        <td className="action-column">
                          <Button variant="danger" size="sm" onClick={() => deleteEntry('file', source.id)}>Delete</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Col>
          </Row>

          <Row className="my-3">
            <Col>
              <h2 className="table-title">FAQ Sources</h2>
              <Form className="d-flex mb-3 search-bar">
                <FormControl
                  type="search"
                  placeholder="Search"
                  className="me-2"
                  value={searchFaq}
                  onChange={(e) => setSearchFaq(e.target.value)}
                />
                <Button variant="outline-success" onClick={() => searchEntries('faq', searchFaq)}>Search</Button>
              </Form>
              <div className="table-wrapper">
                <Table responsive striped hover className="table-sm">
                  <thead className="thead-light">
                    <tr>
                      <th className="id-column">ID</th>
                      <th className="question-column">Question</th>
                      <th className="answer-column">Answer</th>
                      <th className="action-column">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {faqSources.map((source) => (
                      <tr key={source.id}>
                        <td className="id-column">{source.id}</td>
                        <td className="question-column">{source.question}</td>
                        <td className="answer-column">{source.answer}</td>
                        <td className="action-column">
                          <Button variant="danger" size="sm" onClick={() => deleteEntry('faq', source.id)}>Delete</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default App;
