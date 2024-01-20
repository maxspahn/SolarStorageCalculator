const FIELDS_MAP = {
  'internal_supply': 1,
  'external_supply': 2,
  'consumption': 3,
  'feed-in': 4,
  'self-consumption': 5,
  'generation': 6,
};

class DataParser {
  constructor() {
    this._header = [];
    this._data = [];
    this._interval = 1.0;
    this._length = 24 * 4;
  }

  parse_filename(file_name) {
    Papa.parse(file_name, {
      delimiter: ';',
      complete: (result) => {
        this._data = result.data.slice(1,-1);
        this._header = this._data[0];
        this._interval = parseInt(this._data[0][0].split('"|:')[2]) / 60;
        this._length = this._data.length - 1;
      }
    });
  }
  parse(file_content) {
    Papa.parse(file_content, {
        delimiter: ';',
        complete: (result) => {
            this._data = result.data.slice(1,-1);
            this._header = this._data[0];
            this._interval = parseInt(this._data[0][0].split('"|:')[2]) / 60;
            this._length = this._data.length - 1;
        }
    });
  }

  length() {
    return this._length;
  }

  data() {
    return this._data;
  }

  interval() {
    return this._interval;
  }

  dataByTimeAndField(timestamp, field) {
    const index = Math.floor(timestamp * 4) - 1;
    return parseFloat(this._data[index][FIELDS_MAP[field]]);
  }

  dataByField(field) {
    return this._data.map(row => {
        const fieldValue = row[FIELDS_MAP[field]];
        if (fieldValue.includes(',')) {
            return parseFloat(fieldValue.replace(',', ''));
        } else {
          return parseFloat(fieldValue);
        }
    });

  }

  dataByFields(fields) {
    return fields.map(field => this.dataByField(field));
  }

  times() {
    return Array.from({ length: this._length }, (_, i) => `${i*24/96}`);
  }

  header() {
    return this._header;
  }
}

class Storage {
  constructor(initial_charge, interval, capacity) {
    this._charge = [];
    this._feedIn = [];
    this._external = [];
    this._capacity = capacity;
    this._interval = interval;
    this._initialCharge = initial_charge;
  }

  setProductionConsumption(production, consumption) {
    if (production.length !== consumption.length) {
      throw new Error("Length of production and consumption arrays must be equal");
    }

    let currentCharge = this._initialCharge;
    for (let i = 0; i < production.length; i++) {
      const gainedCharge = this._interval * (production[i] - consumption[i]);
      currentCharge += gainedCharge;
      const external = Math.max(0, 0 - currentCharge);
      const feedIn = Math.max(0, currentCharge - this._capacity);
      currentCharge = Math.min(this._capacity, currentCharge);
      currentCharge = Math.max(0, currentCharge);

      this._charge.push(currentCharge);
      this._feedIn.push(feedIn / this._interval);
      this._external.push(external / this._interval);
    }
  }

  get charge() {
    return this._charge;
  }

  get feedIn() {
    return this._feedIn;
  }

  get sumFeedIn() {
    return this.feedIn.reduce((sum, value) => sum + value, 0) * this._interval;
  }

  get external() {
    return this._external;
  }

  get sumExternal() {
    return this.external.reduce((sum, value) => sum + value, 0) * this._interval;
  }
}

