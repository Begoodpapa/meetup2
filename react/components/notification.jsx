var React = require('react');
import { connect } from 'react-redux';
var ReactDOM = require('react-dom');
var NotificationSystem = require('react-notification-system');

var MyComponent = React.createClass({
  _notificationSystem: null,


  componentDidMount: function() {
    this._notificationSystem = this.refs.notificationSystem;
    const {pubsub} = this.props
    const _notificationSystem = this._notificationSystem
    pubsub.subscribe('NOTIFY', function (context, a) {
      //console.log("event!!!!")
      //console.log(a, context)

      _notificationSystem.addNotification({
        message: a.message,
        level: a.level,
        position: "br"
      })
    });

    //pubsub.publish('event', null, 1);
  },

  render: function() {
    return (
      <div>
        <NotificationSystem ref="notificationSystem" />
      </div>
      );
  }
});


export default connect((state, ownProps) => ({
  pubsub: state.pubsub
}), {} )(MyComponent);
