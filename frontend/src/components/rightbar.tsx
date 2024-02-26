import '@fortawesome/fontawesome-svg-core/styles.css'
import style from './rightbar.module.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { Card, Form, InputGroup } from 'react-bootstrap'


export default function Rightbar() {
    return <>
        <div className={"main"}>
            <nav className={style.rightnav}>
                <InputGroup className={["mr-sm-2", style.bottomMargin, style.topMargin].join(' ')}>
                    <InputGroup.Text  className={[style.searchBar1].join(' ')}><FontAwesomeIcon icon={faSearch} fixedWidth/></InputGroup.Text>
                    <Form.Control type="text" placeholder="Search"  className={[style.searchBar2].join(' ')}>
                </Form.Control>                        
                </InputGroup>
   

                <Card className={[style.bottomMargin, style.boxes].join(' ')}>
      <Card.Body>This is some text within a card body.</Card.Body>
                </Card>
                <Card className={[style.bottomMargin, style.boxes].join(' ')}>
      <Card.Body>This is some text within a card body.</Card.Body>
                </Card>
                <Card className={[style.bottomMargin, style.boxes].join(' ')}>
      <Card.Body>This is some text within a card body.</Card.Body>
    </Card>
            </nav>               
        </div>
    </>;
}
