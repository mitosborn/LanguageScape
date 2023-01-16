import Form from 'react-bootstrap/Form';
import {Col, Row} from "react-bootstrap";

function SelectLanguageDropdown() {
    return (
        <Form>
            <Form.Group as={Row} className="mb-3" controlId="formPlaintextPassword">
                <Form.Label column sm={"4"}>
                    <h5 style={{"whiteSpace": "nowrap"}}>
                        I speak:
                    </h5>
                </Form.Label>
                <Col>
                    <Form.Select>
                        <option>Disabled select</option>
                    </Form.Select>
                </Col>
            </Form.Group>
        </Form>
    );
}

export default SelectLanguageDropdown;