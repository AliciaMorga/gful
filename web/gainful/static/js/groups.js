GG.Groups = (function() {
  var me = {};

  console.log("Welcome to Gainful");
  me.onCreateGroupClicked = function() {
    console.log("new group");
    var modal = document.getElementById("newGroupModal")
    if (modal.style.display == 'none') {
      modal.style.display = 'flex';
    } else {
      modal.style.display = 'none';
    }
  };

  me.onGroupEdit = function(e) {
    console.log("group", e);
  };

  return me;
})();

var GroupsPage = React.createClass({
  getInitialState: function() {
    return {
      'selected': -1,
    };
  },  
  onCreateGroupClicked: function() {
    console.log("group create clicked");
    $("#newGroupModal").show();
  },

  onGroupEditClicked: function(groupId) {
    console.log("group clicked ", groupId);
    this.setState({'selected': groupId});
  },

  render: function() {
    let page = <GroupsList onCreate={this.onCreateGroupClicked} onEdit={this.onGroupEditClicked}/>;
    if (this.state.selected >= 0) {
      page = <GroupView groupId={this.state.selected}/>;
    }
    return (
      <div className="u-pad-s">
        {page}
      </div>
    );
  },
});

var GroupsList = React.createClass({
  getInitialState: function() {
    return {data: {}};
  },
  componentDidMount: function() {
    $.ajax({
      url: `/groups`,
      dataType: 'json',
      cache: false,
      success: function(data) {
        console.log('successful /groups', data)
        this.setState({data: data.data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }.bind(this)
    });
  },

  _onEditClicked(group_id) {
    this.props.onEdit(group_id);
  },

  render: function() {
    let that = this;
    console.log("render", this.state.data)
    let groups = this.state.data.groups || [];
    let groupRows = groups.map(function(group) {
      if (group.name) {
        console.log("adding group", group.name);
        let numMembers = "no";
        if (group.members) {
          numMembers = group.members.length;
        }
        var boundClick = that._onEditClicked.bind(that, group.id);

        return (
          <tr key={group.id}>
            <td>{group.id}</td>
            <td>{group.name}</td>
            <td>{numMembers} members</td>
            <td><button className="c-btn c-btn--secondary u-l-fr" onClick={boundClick}>Edit</button></td>
          </tr>
        )
      }
    });

    return (
      <div>
        <h2 className="u-l-fl">Groups</h2>
        <div className="page-menu u-l-fr">
            <button id="newGroupBtn" className="c-btn c-btn--primary" onClick={this.props.onCreate}>Create group</button>
        </div>
        <table className="c-table c-table--selectable">
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th>Members</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {groupRows}
          </tbody>
        </table>
      </div>
    );
  }
});


var GroupMemberList = React.createClass({
  render: function() {
  	let members = this.props.members || [];

    let memberRows = members.map(function(member) {
      return (
	    <tr>
	      <td>1</td>
	      <td>{member.name}</td>
	      <td><a href="https://gif.daneden.me/tina_five.gif">Tina Fey giving herself a high-five</a></td>
	    </tr>
      );
    });
    return (
      <div className="groupMemberList">
      	<table className="c-table c-table--zebra">
		  <thead>
		  	<tr>
			    <th>#</th>
			    <th>Name</th>
			    <th>Mobile Number</th>
		    </tr>
		  </thead>
		  <tbody>
        	{memberRows}
          </tbody>
         </table>
      </div>
    );
  }
});

var GroupView = React.createClass({
  getInitialState: function() {
    return {data: [], adding: false};
  },
  componentDidMount: function() {
    $.ajax({
      url: `/groups/${this.props.groupId}`,
      dataType: 'json',
      cache: false,
      success: function(data) {
      	console.log('successful xhr', data)
        this.setState({data: data.data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  
  onAddMemberClicked: function() {
    console.log("addMemberClicked");
    this.setState({adding: true});
  },

  onSave: function(userIds) {
    console.log("onSave ", userIds);
    this.setState({adding: false});
  },

  render: function() {
    let addModal = null;
    if (this.state.adding) {
      console.log("adding addingModal");
      addModal = <AddMemberModal groupId={this.props.groupId} members={this.state.data.members} onSave={this.onSave}/>;
    }
    return (
      <div>
        <h2 className="u-l-fl">{this.state.data.name}</h2>
        <div className="clearfix page-menu">
          <button id="addMemberButton" className="c-btn c-btn--primary u-l-fr" onClick={this.onAddMemberClicked}>Add members</button>
        </div>
        <GroupMemberList members={this.state.data.members} />
        {addModal}
      </div>
    );
  }
});

var AddMemberModal = React.createClass({
  getInitialState: function() {
    return {membersToAdd: []};
  },

  saveMembers: function() {
    this.props.onSave();
    $.ajax({
      url: `/groups/${this.props.groupId}/members/add`,
      type: 'POST',
      dataType: 'json',
      data: {member_ids : this.state.membersToAdd},
      cache: false,
      success: function(data) {
        console.log('successful xhr', data)
        this.setState({data: data.data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  onSelect: function(userId) {
    var membersToAdd = this.state.membersToAdd;
    membersToAdd.push(userId);
    this.setState({'membersToAdd': membersToAdd});
    console.log("selected ", userId, this.state.membersToAdd);
  },

  render: function() {
    return (
      <div id="addMemberModal" className="c-modal-overlay">
        <div className="c-modal">
          <div className="c-modal__header">
            <h2>Add members</h2>
          </div>
          <div className="c-modal__content">
            <UserList selected={this.props.members} membersToAdd={this.state.membersToAdd} onSelect={this.onSelect} onSave={this.saveMembers}/>
          </div>
        </div>
      </div>
    );
  }
});

var UserList = React.createClass({
  getInitialState: function() {
    return {data: {}};
  },
  componentDidMount: function() {
    let groupId = 1;
    $.ajax({
      url: `/users`,
      dataType: 'json',
      cache: false,
      success: function(data) {
        console.log('successful /users', data)
        this.setState({data: data.data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }.bind(this)
    });
  },

  isInMembers: function(user) {
    // TODO: store as map
    if (this.props.members) {
      for (var i=0; i<this.props.members.length; i++) {
        if (this.props.members[i].id == user.id) {
          return true;
        }
      }
    }

    // Check unsaved members too
    if (this.props.membersToAdd) {
      for (i=0; i< this.props.membersToAdd.length; i++) {
        if (this.props.membersToAdd[i] == user.id) {
          return true;
        }
      }
    }
    return false;
  },

  _onSelect(user_id) {
    this.props.onSelect(user_id);
  },

  render: function() {
    let that = this;
    console.log("render", this.state.data, this.props);
    let users = this.state.data.users || [];
    let userRows = users.map(function(user) {
      if (user.mobile_number) {
        var boundClick = that._onSelect.bind(that, user.id);
        var disabled = that.isInMembers(user);
        var button = <button className="c-btn c-btn--primary u-l-fr" onClick={boundClick}>Add</button>
        var trSelect = "";
        if (disabled) {
          console.log("found a disabled one")
          button = <button className="c-btn c-btn--primary c-btn--disabled u-l-fr" onClick={boundClick}>Add</button>
          trSelect = "is-selected";
        }
        return (
          <tr key={user.id} className={trSelect} onClick={boundClick}>
            <td>{user.id}</td>
            <td>{user.name}</td>
            <td>{user.mobile_number}</td>
            <td>{button}</td>
          </tr>
        )
      }
    });

    return (
      <div className="user-list">
        <h2 className="u-l-fl">Users</h2>
        <button className="c-btn c-btn--primary u-l-fr" onClick={this.props.onSave}>Save</button>
        <table className="c-table c-table--selectable">
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th>Mobile Number</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {userRows}
          </tbody>
        </table>
      </div>
    );
  }
});



ReactDOM.render(
  React.createElement(GroupsPage, null),
  document.getElementById('groups_content')
);

$("#group_content").hide();
