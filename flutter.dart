import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'User Type Form',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: UserTypeForm(),
    );
  }
}

class UserTypeForm extends StatefulWidget {
  @override
  _UserTypeFormState createState() => _UserTypeFormState();
}

class _UserTypeFormState extends State<UserTypeForm> {
  final _formKey = GlobalKey<FormState>();
  String? _userType = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('User Type Form'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                'Are you a buyer or a seller?',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              RadioListTile(
                title: Text('Buyer'),
                value: 'buyer',
                groupValue: _userType,
                onChanged: (value) {
                  setState(() {
                    _userType = value as String?;
                  });
                },
              ),
              RadioListTile(
                title: Text('Seller'),
                value: 'seller',
                groupValue: _userType,
                onChanged: (value) {
                  setState(() {
                    _userType = value as String?;
                  });
                },
              ),
              SizedBox(height: 16.0),
              ElevatedButton(
                onPressed: () {
                  if (_userType != null && _userType!.isNotEmpty) {
                    // Navigate to respective form based on user type
                    if (_userType == 'buyer') {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => BuyerDetailsForm()),
                      );
                    } else if (_userType == 'seller') {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => SellerDetailsForm()),
                      );
                    }
                  }
                },
                child: Text('Next'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class BuyerDetailsForm extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Buyer Details Form'),
      ),
      body: Center(
        child: Text('Buyer Details Form'),
      ),
    );
  }
}

class SellerDetailsForm extends StatefulWidget {
  @override
  _SellerDetailsFormState createState() => _SellerDetailsFormState();
}

class _SellerDetailsFormState extends State<SellerDetailsForm> {
  final _formKey = GlobalKey<FormState>();
  TextEditingController _nameController = TextEditingController();
  TextEditingController _shopNameController = TextEditingController();
  TextEditingController _locationController = TextEditingController();
  TextEditingController _shopTypeController = TextEditingController();
  TextEditingController _pincodeController = TextEditingController();
  bool _isDeliveryAvailable = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Seller Details Form'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                'Seller Details',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(labelText: 'Name'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your name';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _shopNameController,
                decoration: InputDecoration(labelText: 'Shop Name'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your shop name';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _locationController,
                decoration: InputDecoration(labelText: 'Location'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter your shop location';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _shopTypeController,
                decoration: InputDecoration(labelText: 'Type of Shop'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter the type of your shop';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _pincodeController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'Pincode'),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter the pincode of your area';
                  } else if (value.length != 6) {
                    return 'Pincode must be 6 digits long';
                  }
                  return null;
                },
              ),
              Row(
                children: <Widget>[
                  Text('Delivery Available?'),
                  Checkbox(
                    value: _isDeliveryAvailable,
                    onChanged: (value) {
                      setState(() {
                        _isDeliveryAvailable = value!;
                      });
                    },
                  ),
                ],
              ),
              SizedBox(height: 16.0),
              ElevatedButton(
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    // Process the form data
                    // For example, you can save the data to a database
                    // or send it to an API
                    print('Form submitted');
                  }
                },
                child: Text('Submit'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}