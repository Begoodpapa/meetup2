import React from 'react';
import ReactDOM from 'react-dom';
import { connect } from 'react-redux';
import Header from 'components/header/header';
import Footer from 'components/footer/footer';
import GroupArr from 'components/group/grouparray';
import { Button, Grid, Col, Row, Panel, DropdownButton, MenuItem, Thumbnail } from "react-bootstrap";
import { hashHistory } from 'react-router';
var _ = require("lodash");
require('../../assets/styles/homePage.css');
var $ = require('jquery');

class Main extends React.Component {

  render() {

    return(
      <div>
        <header>
          <Header allHeaderClasses={["find", "meetup"]} />
        </header>
        <section id="service">        
          <Grid>
            <Row>
              <Col md={6} mdOffset={3}>
                <br/>
                <h3 style={{"textAlign":"center"}}> Beehive is </h3>
                <p style={{"textAlign":"center"}}> designed for us to find <em><b>interesting</b></em> communities and events for <em><b>sharing</b></em> and <em><b>learning</b></em>. </p>
                <br/>
              </Col>
            </Row>
            <Row>
              <div style={{"minHeight":"50px"}}>
              </div>
            </Row>

            <div className="container">
              <div className="row hottest" id = "row-content">
                <h2 className="section-title">Popular</h2>
                <div id="populargroups">
                  <GroupArr 
                    type = 'hottest'
                  />
                </div>
              </div>
            </div> 

            <div className="container">
              <div className="row latest" id = "row-content">
                <h2 className="section-title">Latest</h2>
                <div id="latestgroups">
                  <GroupArr 
                    type = 'latest'
                  />                 
                </div>
              </div>
            </div>           
          
            <div className="container">
              <div className="row all" id = "row-content">
                <h2 className="section-title">All</h2>
                <div id="allgroups">
                  <GroupArr 
                    type = 'all'
                  />          
                </div>
              </div>
            </div>    
                                 
            <Row>
              <div style={{"minHeight":"50px"}}>
              </div>
            </Row>
          </Grid>
          <Footer/>
        </section>
      </div>
    )
  }
}

export default Main;