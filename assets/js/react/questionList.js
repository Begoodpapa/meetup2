'use strict';
var QuestionRow = React.createClass({
  displayName: 'QuestionRow',
  render: function() {

    var answer = this.props.qa.answer ? ( React.createElement("div", null, " ", React.createElement("div", null, " Answer "), React.createElement("p", null, this.props.qa.answer), " ")) : (React.createElement("div", null, "No answer ye ") )

    return ( React.createElement("div", null, 
      React.createElement("div", null, " Question "), " ", React.createElement("p", null, " ", 
      this.props.qa.question, 
    " "), " ", 
    answer, 
  " ")
);
}
});


var QuetsionList = React.createClass({
  displayName: 'QuetsionList',

  render: function() {
    var list = this.props.qas.map(function(qa) {
      return ( React.createElement(QuestionRow, {qa: 
          qa
        }
        )
      );
    });

    return ( React.createElement("div", null, 
      React.createElement("div", null, " QuetsionList "), " ", React.createElement("ul", null, " ", 
      list, 
    " "), " ")
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
        } catch (e) {

        }

        var onMessage = this.onMessage.bind(this);

        io.socket.get('/chat', onMessage);

        io.socket.on('message', onMessage);

        return {
          qas: [],
          status: 'disconnect'
        };
      },
      render: function() {
        return ( React.createElement(QuetsionList, {qas: 
            this.state.qas
          }
          ));
        }
      });



    $(function() {

      React.render( React.createElement(QAHolder, null/) ,
        document.getElementById('myroom'));
    })