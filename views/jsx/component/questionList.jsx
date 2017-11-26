'use strict';
var QuestionRow = React.createClass({
  displayName: 'QuestionRow',
  render: function() {

    var answer = this.props.qa.answer ? (<div>
                                           <div> Answer
                                           </div>
                                           <p>{this.props.qa.answer}</p>
                                         </div>) : (<div>No answer ye </div>)

    return (<div>
              <div> Question
              </div>
              <p> { this.props.qa.question }
              </p> { answer }
            </div>
    );
  }
});


var QuetsionList = React.createClass({
  displayName: 'QuetsionList',

  render: function() {
    var list = this.props.qas.map(function(qa) {
      return (<QuestionRow qa={ qa } />
      );
    });

    return (<div>
              <div> QuetsionList
              </div>
              <ul> { list }
              </ul>
            </div>
    );
  }
});

var QAHolder = React.createClass({
  displayName: 'QAHolder',

  onMessage: function(qas) {
    var arr;
    if (!$.isArray(qas)) {
      arr = [qas];
    }

    this.setState({
      qas: arr,
      connected: true
    })
  },


  getInitialState: function() {
    var connected = false;
    try {
      connected = io.socket.socket.connected;
    } catch (e) {}

    var onMessage = this.onMessage.bind(this);

    io.socket.get('/chat', onMessage);

    io.socket.on('message', onMessage);

    return {
      qas: [],
      status: 'disconnect'
    };
  },
  render: function() {
    return (<QuetsionList qas={ this.state.qas } />);
  }
});


$(function() {

  React.render(<QAHolder />,
    document.getElementById('myroom'));
})