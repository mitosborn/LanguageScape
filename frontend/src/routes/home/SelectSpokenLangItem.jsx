import {ListGroup} from "react-bootstrap";
import {Link} from "react-router-dom";
import styled from "styled-components";

const Item = styled.div`
    text-decoration: none;
`

export default function SelectSpokenLangItem({language, link}) {
    return (
        <Item as={Link} to={link}>
            <ListGroup.Item action>
                {language}
            </ListGroup.Item>
        </Item>
    )
}