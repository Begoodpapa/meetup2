import { connect } from 'react-redux'; 
import React from 'react'; 
import {Jumbotron, Grid, Row, Col} from "react-bootstrap";
var _ = require("lodash");
var $ = require('jquery');

class Header extends React.Component {

  constructor(props){
    super(props);

    this.state = {
      headerClass: "find"
    }
  }


  componentDidMount(){
    var {allHeaderClasses} = this.props

    this.setState({
      headerClass: allHeaderClasses[0]
    })

    this.intervalId = setInterval( ()=>{
      var that = this;
      $('.'+this.state.headerClass).fadeOut("slow", function(){

        var {allHeaderClasses} = that.props
        that.setState({
          headerClass: that.getHeaderClass(allHeaderClasses)
        });
        $('.'+that.state.headerClass).fadeIn();

      });
      
    }, 8000)

  }

  getHeaderClass = (allHeaderClasses)=> _.sampleSize(allHeaderClasses, 1)

  componentWillUnmount(){
    clearInterval(this.intervalId);
  }
  
  render(){
    
    return (
      <div className={this.state.headerClass} id="home" >
        <Col>
          <Jumbotron className="overlay" id="find">

            <Row>
                <Col md={8} mdOffset={2}>
                            
                  <Col md={12}>
                    <h1 id="intro"> <span style={{"color": "#ffffff"}} >Beehive</span></h1>
                    <h2>a meetup society</h2>
                  </Col>
                         
                </Col>
            </Row>

          </Jumbotron>
        </Col>
      </div>
    )
 }

}

export default Header