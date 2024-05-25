import React, { useState, useEffect } from 'react';
import { Table, Button, Form, FormControl, Container, Row, Col, Card, Modal } from 'react-bootstrap';
import axios from 'axios';
import debounce from 'lodash.debounce'; // Import debounce from lodash
import './App.css'; // Import the custom CSS file

const App = () => {
  const [urlSources, setUrlSources] = useState([]);
  const [fileSources, setFileSources] = useState([]);
  const [faqSources, setFaqSources] = useState([]);
  const [searchUrl, setSearchUrl] = useState('');
  const [searchFile, setSearchFile] = useState('');
  const [searchFaq, setSearchFaq] = useState('');

  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [modalData, setModalData] = useState({});

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const urlResponse = await axios.get('http://localhost:8000/detibot/url_sources');
      const fileResponse = await axios.get('http://localhost:8000/detibot/file_sources');
      const faqResponse = await axios.get('http://localhost:8000/detibot/faq_sources');
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
      if (query === '') {
        fetchData();
        return;
      }

      console.log(`Searching ${type} with query:`, query);
      const response = await axios.get(endpoints[type]);
      console.log(`Response for ${type}:`, response.data);

      if (type === 'url') setUrlSources(response.data);
      if (type === 'file') setFileSources(response.data);
      if (type === 'faq') setFaqSources(response.data);
    } catch (error) {
      console.error(`Error searching ${type} entries`, error);
    }
  };

  const debouncedSearchUrl = debounce((query) => searchEntries('url', query), 300);
  const debouncedSearchFile = debounce((query) => searchEntries('file', query), 300);
  const debouncedSearchFaq = debounce((query) => searchEntries('faq', query), 300);

  useEffect(() => {
    debouncedSearchUrl(searchUrl);
  }, [searchUrl]);

  useEffect(() => {
    debouncedSearchFile(searchFile);
  }, [searchFile]);

  useEffect(() => {
    debouncedSearchFaq(searchFaq);
  }, [searchFaq]);

  const handleShowModal = (type, data) => {
    setModalType(type);
    setModalData(data);
    setShowModal(true);
  };

  const handleCloseModal = () => setShowModal(false);

  const handleUpdate = async () => {
    const { id } = modalData;
    const endpoints = {
      url: `http://localhost:8000/detibot/update_urlsource/${id}`,
      file: `http://localhost:8000/detibot/update_filesource/${id}`,
      faq: `http://localhost:8000/detibot/update_faqsource/${id}`,
    };

    try {
      if (modalType === 'url') {
        const updateData = {
          ...modalData,
          wait_time: 3,
          update_period_id: {
            Daily: 1,
            Weekly: 2,
            Monthly: 3,
            Quarterly: 4,
          }[modalData.update_period],
        };
        await axios.put(endpoints.url, updateData);
      } else if (modalType === 'file') {
        const formData = new FormData();
        formData.append('file', modalData.file);
        formData.append('descript', modalData.description);
        await axios.put(endpoints.file, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      } else if (modalType === 'faq') {
        await axios.put(endpoints.faq, modalData);
      }
      fetchData();
      handleCloseModal();
    } catch (error) {
      console.error(`Error updating ${modalType} entry`, error);
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
              </Form>
              <div className="table-wrapper">
                <Table responsive striped hover className="table-sm url-table">
                  <thead className="thead-light">
                    <tr>
                      <th className="id-column">ID</th>
                      <th className="url-column">URL</th>
                      <th className="description-column">Description</th>
                      <th className="paths-column">Paths</th>
                      <th className="update-period-column">Update Period</th>
                      <th className="action-column">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {urlSources.map((source) => (
                      <tr key={source.id}>
                        <td className="id-column">{source.id}</td>
                        <td className="url-column">{source.url}</td>
                        <td className="description-column">{source.description}</td>
                        <td className="paths-column">{source.paths.join(', ')}</td>
                        <td className="update-period-column">{source.update_period}</td>
                        <td className="action-column">
                          <Button variant="danger" size="sm" onClick={() => deleteEntry('url', source.id)}>Delete</Button>
                          <Button className="update-button" size="sm" onClick={() => handleShowModal('url', source)}>Update</Button>
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
                          <Button className="update-button" size="sm" onClick={() => handleShowModal('file', source)}>Update</Button>
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
                          <Button className="update-button" size="sm" onClick={() => handleShowModal('faq', source)}>Update</Button>
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

      {/* Modal */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Update {modalType.charAt(0).toUpperCase() + modalType.slice(1)} Source</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {modalType === 'url' && (
            <Form>
              <Form.Group controlId="formUrl">
                <Form.Label>URL</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.url || ''}
                  onChange={(e) => setModalData({ ...modalData, url: e.target.value })}
                />
              </Form.Group>
              <Form.Group controlId="formDescription">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.description || ''}
                  onChange={(e) => setModalData({ ...modalData, description: e.target.value })}
                />
              </Form.Group>
              <Form.Group controlId="formPaths">
                <Form.Label>Paths</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.paths || ''}
                  onChange={(e) => setModalData({ ...modalData, paths: e.target.value.split(', ') })}
                />
              </Form.Group>
              <Form.Group controlId="formUpdatePeriod">
                <Form.Label>Update Period</Form.Label>
                <Form.Control
                  as="select"
                  value={modalData.update_period || ''}
                  onChange={(e) => setModalData({ ...modalData, update_period: e.target.value })}
                >
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Monthly</option>
                  <option>Quarterly</option>
                </Form.Control>
              </Form.Group>
              <Form.Group controlId="formRecursive">
                <Form.Check
                  type="checkbox"
                  label="Recursive"
                  checked={modalData.recursive || false}
                  onChange={(e) => setModalData({ ...modalData, recursive: e.target.checked })}
                />
              </Form.Group>
            </Form>
          )}
          {modalType === 'file' && (
            <Form>
              <Form.Group controlId="formFileDescription">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.description || ''}
                  onChange={(e) => setModalData({ ...modalData, description: e.target.value })}
                />
              </Form.Group>
              <Form.Group controlId="formFile">
                <Form.Label>Upload New File</Form.Label>
                <Form.Control
                  type="file"
                  onChange={(e) => setModalData({ ...modalData, file: e.target.files[0] })}
                />
              </Form.Group>
            </Form>
          )}
          {modalType === 'faq' && (
            <Form>
              <Form.Group controlId="formQuestion">
                <Form.Label>Question</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.question || ''}
                  onChange={(e) => setModalData({ ...modalData, question: e.target.value })}
                />
              </Form.Group>
              <Form.Group controlId="formAnswer">
                <Form.Label>Answer</Form.Label>
                <Form.Control
                  type="text"
                  value={modalData.answer || ''}
                  onChange={(e) => setModalData({ ...modalData, answer: e.target.value })}
                />
              </Form.Group>
            </Form>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Close
          </Button>
          <Button variant="primary" onClick={handleUpdate}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default App;
