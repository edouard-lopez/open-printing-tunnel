import test from 'ava';
import filter from '../src/components/scan.filters';
import mockScan from './nmap_snmp.mock.json';

const mockOtherSnmpInfos = {
  pageCount: { value: '' },
  sysContact: { value: '' },
  sysDescription: { value: '' },
  sysName: { value: '' },
  uptime: { value: '' }
};
const mockSnmpInfosString =
  '\t# pageCount: \tsysContact: \tsysDescription: \tsysName: \tuptime: ';

test('should format printer infos as list of raw text', t => {
  const printers = {
    '192.168.2.250': {
      hostname: '192.168.2.250',
      port: 9100,
      description: { value: 'Brother HL-5250DN series' },
      ...mockOtherSnmpInfos
    }
  };

  const clipboard = filter.toLog(printers);

  t.deepEqual(clipboard, [
    'Brother HL-5250DN series\t192.168.2.250\t9100' + mockSnmpInfosString
  ]);
});
test("should format printer's with empty description", t => {
  const printers = {
    '192.168.2.250': {
      hostname: '192.168.2.250',
      port: 9100,
      description: { value: '' },
      ...mockOtherSnmpInfos
    }
  };
  const clipboard = filter.toLog(printers);

  t.deepEqual(clipboard, ['\t192.168.2.250\t9100' + mockSnmpInfosString]);
});

test("should format all printer's infos as list of raw text", t => {
  const printers = mockScan.devices;

  const clipboard = filter.toLog(printers);

  t.is(clipboard.length, 1);
  t.is(
    clipboard[0],
    'Brother HL-5250DN series\t192.168.2.250\t9100\t# ' +
      'pageCount: 22629\t' +
      'sysContact: \t' +
      'sysDescription: Brother NC-6400h, Firmware Ver.1.01  (05.08.31),MID 84UZ92\t' +
      'sysName: BRN_7D3B43\t' +
      'uptime: 169046170'
  );
});

test('should format toLog as raw text', t => {
  const clipboard = [
    'description\t10.0.1.7\t9100',
    'description\t10.0.1.8\t9100'
  ];

  const text = filter.text(clipboard);

  t.is(text, 'description\t10.0.1.7\t9100\ndescription\t10.0.1.8\t9100');
});

test('should remove text after #', t => {
  const printers = {
    '192.168.2.250': {
      hostname: '192.168.2.250',
      port: 9100,
      description: { value: '' },
      ...mockOtherSnmpInfos
    }
  };
  const clipboard = filter.toClipboard(printers);

  t.deepEqual(clipboard, ['\t192.168.2.250\t9100']);
});
