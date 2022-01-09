import React, { Component } from 'react';
import { Table } from 'react-bootstrap';

import { Button, ButtonToolbar, Image } from 'react-bootstrap';
import { AddEmpModal } from './AddEmpModal';
import { EditEmpModal } from './EditEmpModal';
import {createMuiTheme, ThemeProvider} from '@material-ui/core';
import AudioPlayer from 'material-ui-audio-player';
const muiTheme = createMuiTheme({ });
export class Employee extends Component {

    constructor(props) {
        super(props);
        this.state = { emps: [], addModalShow: false, editModalShow: false }
    }

    refreshList() {
        fetch(process.env.REACT_APP_API + 'employee')
            .then(response => response.json())
            .then(data => {
                this.setState({ emps: data });
            });
    }

    componentDidMount() {
        this.refreshList();
    }

    componentDidUpdate() {
        this.refreshList();
    }

    deleteEmp(empid) {
        if (window.confirm('Are you sure?')) {
            fetch(process.env.REACT_APP_API + 'employee/' + empid, {
                method: 'DELETE',
                header: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
        }
    }
    render() {
        const { emps, empid, empname, depmt, photofilename, doj } = this.state;
        let addModalClose = () => this.setState({ addModalShow: false });
        let editModalClose = () => this.setState({ editModalShow: false });
        return (
            <div >
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                            <th>EmployeeId</th>
                            <th>EmployeeName</th>
                            <th>Department</th>
                            <th>DOJ</th>
                            <th>AudioText</th>
                            <th>AudioSummary</th>
                            <th>profile</th>
                            <th>Options</th>
                        </tr>
                    </thead>
                    <tbody>
                        {emps.map(emp =>
                            <tr key={emp.EmployeeId}>
                                <td>{emp.EmployeeId}</td>
                                <td>{emp.EmployeeName}</td>
                                <td>{emp.Department}</td>
                                <td>{emp.DateOfJoining}</td>
                                <td>{emp.AudioText}</td>
                                <td>{emp.AudioSummary}</td>
                                {/* <td><Image width="200px" height="200px"
                                    src={process.env.REACT_APP_PHOTOPATH + emp.PhotoFileName} /></td> */}
                                <td>
                                    
                                    <ThemeProvider theme={muiTheme}>
                                        <AudioPlayer src={process.env.REACT_APP_PHOTOPATH + emp.PhotoFileName} />
                                    </ThemeProvider>
                                    </td>
                                <td>
                                    <ButtonToolbar>
                                        <Button className="mr-2" variant="info"
                                            onClick={() => this.setState({
                                                editModalShow: true,
                                                empid: emp.EmployeeId, empname: emp.EmployeeName, depmt: emp.Department,
                                                photofilename: emp.PhotoFileName, doj: emp.DateOfJoining
                                            })}>
                                            Edit
                                        </Button>

                                        <Button className="mr-2" variant="danger"
                                            onClick={() => this.deleteEmp(emp.EmployeeId)}>
                                            Delete
                                        </Button>

                                        <EditEmpModal show={this.state.editModalShow}
                                            onHide={editModalClose}
                                            empid={empid}
                                            empname={empname}
                                            depmt={depmt}
                                            photofilename={photofilename}
                                            doj={doj}
                                        />
                                    </ButtonToolbar>

                                </td>

                            </tr>)}
                    </tbody>

                </Table>

                <ButtonToolbar>
                    <Button variant='primary'
                        onClick={() => this.setState({ addModalShow: true })}>
                        Add Employee</Button>

                    <AddEmpModal show={this.state.addModalShow}
                        onHide={addModalClose} />
                </ButtonToolbar>
            </div>
        )
    }
}