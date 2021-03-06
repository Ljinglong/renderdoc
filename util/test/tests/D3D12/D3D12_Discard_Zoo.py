import rdtest
import struct
import renderdoc as rd


class D3D12_Discard_Zoo(rdtest.Discard_Zoo):
    demos_test_name = 'D3D12_Discard_Zoo'
    internal = False

    def __init__(self):
        rdtest.Discard_Zoo.__init__(self)

    def check_capture(self):
        self.check_textures()

        draw = self.find_draw("TestStart")

        self.check(draw is not None)

        self.controller.SetFrameEvent(draw.eventId, True)

        # Check the buffer
        for res in self.controller.GetResources():
            if res.name == "Buffer":
                data: bytes = self.controller.GetBufferData(res.resourceId, 0, 0)

                self.check(all([b == 0x88 for b in data]))

        draw = self.find_draw("TestEnd")

        self.check(draw is not None)

        self.controller.SetFrameEvent(draw.eventId, True)

        # Check the buffer
        for res in self.controller.GetResources():
            if res.name == "Buffer":
                data: bytes = self.controller.GetBufferData(res.resourceId, 0, 0)

                data_u32 = struct.unpack_from('=256L', data, 0)

                self.check(all([u == 0xD15CAD3D for u in data_u32]))